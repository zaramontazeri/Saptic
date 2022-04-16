#Some utilities to work with django models and foreign keys.
#Especially useful for finding (and writing out) code to illuminate information about relations.
#
#To try it out, run show_relation_accessors(model) in a python prompt, or to be more general, get_related_instance_ids_code(model)
#
#-2011 CBWhiz
#
#
#Usage sample:
#    from django.db import transaction
#
#    c = get_related_objects(HatedModel.objects.filter(id=24576))
#    c.data.keys()
#    [<class 'app1.models.HatedModel'>, <class 'app2.models.MissionCriticalModel'>]
#
#    transaction.enter_transaction_management()
#    exec get_replace_object_relations_code(HatedModel, 24576, 12740)
#    c = get_related_objects(Assembly.objects.filter(id=24576))
#    c.data.keys()
#    [<class 'stock.models.HatedModel'>]
#    transaction.commit()

from django.db.models.deletion import Collector
def get_related_objects(qs, using='default'):
    """Returns a Collector instance whose 'data' attribute is a mapping of Models to a set of dependent instances of that model"""
    c = Collector(using)
    c.collect(qs)
    return c

def get_relations(model, global_accessors=False, instance_filter=True):
    """Returns all (non gfk) foreign key relations to a django model and their accessors"""
    for ro in model._meta.get_all_related_objects(include_hidden=True):
        an = "%s.%s"%('%s', ro.get_accessor_name())
	if an.endswith('+') or global_accessors:
            #m2m
            if instance_filter:
                an = "%s.objects.filter(%s=%s)"%(ro.model.__name__, ro.field.name, '%s')
            else:
                an = "%s.objects.filter(%s__isnull=False)"%(ro.model.__name__, ro.field.name)
        else:
            an += '.all()'
        yield (
		model.__name__,
		ro.field.rel.get_related_field().name,

                ro.model._meta.app_label,
		ro.model.__name__,
                ro.field.name,

                an
        )

def get_relations_gfk(model, global_accessors=False, instance_filter=True):
    for rf in model._meta.many_to_many:
        if not rf.rel.through:
            #rf is a GenericRelation (RelatedField)
            ct = ContentType.objects.get_for_model(model).pk
            if global_accessors:
                an = "%s.objects.filter(%s=%s)"%(rf.rel.to.__name__, rf.content_type_field_name, ct)
                if instance_filter:
                    an += ".filter(%s=%%s)"%(rf.object_id_field_name)
            else:
                an = "%%s.%s.all()"%(rf.name, )
            yield (
		model.__name__,
                rf.m2m_target_field_name(),

                rf.rel.to._meta.app_label,
                rf.rel.to.__name__,
                rf.object_id_field_name,

                rf.content_type_field_name,
                rf.name,

                an,
            )

def get_related_instance_ids_code(model):
    r = list(get_relations(model, True, False)) + list(get_relations_gfk(model, True, False))
    imports = ["from django.db.models.loading import get_model"]
    qsgroups = []
    for i in r:
        imports.append("%s = get_model('%s', '%s')"%(i[3], i[2], i[3]))
        qsgroups.append(i[-1] + '.values_list("%s", flat=True)'%(i[4]))
    ld = locals()
    pycode = '\n'.join(imports) + "\nqslist=[\n\t%s\n]"%(",\n\t".join(qsgroups))
    return pycode

def get_unrelated_instance_qs(model):
    exec get_related_instance_ids_code(model);
    from django.db.models import Q
    filt = []
    for qs in qslist:
        filt.append(~Q(pk__in=qs))
    return model.objects.filter(reduce(lambda x, y: x & y, filt))

def get_replace_object_relations_code(model, oldid, newid):
    """Returns python code that will replace an object's relations to point to a different object (of the same type)"""
    r = list(get_relations(model, True, False)) + list(get_relations_gfk(model, True, False))
    imports = ["from django.db.models.loading import get_model"]
    qsgroups = []
    for i in r:
        imports.append("%s = get_model('%s', '%s')"%(i[3], i[2], i[3]))
        qsgroups.append(i[-1] + '.filter(%s=%s).update(%s=%s)'%(i[4], oldid, i[4], newid))
    ld = locals()
    pycode = '\n'.join(imports) + "\n\n%s"%("\n".join(qsgroups))
    return pycode

def show_relation_accessors(model):
    r = list(get_relations(model)) + list(get_relations_gfk(model))
    for i in r:
        print (i[-1]%('instance'))