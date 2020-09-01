__doc__ = "数组转树"

from pprint import pprint

data = [

    {'id': 1, 'parent_id': 2, 'name': "Node1"},
    {'id': 2, 'parent_id': 5, 'name': "Node2"},
    {'id': 3, 'parent_id': 0, 'name': "Node3"},
    {'id': 4, 'parent_id': 5, 'name': "Node4"},
    {'id': 5, 'parent_id': 0, 'name': "Node5"},  # 关键
    {'id': 6, 'parent_id': 3, 'name': "Node6"},
    {'id': 7, 'parent_id': 3, 'name': "Node7"},
    {'id': 8, 'parent_id': 0, 'name': "Node8"},
    {'id': 9, 'parent_id': 1, 'name': "Node9"}
]


def list_to_tree(data):
    out = {
        0: {'id': 0, 'parent_id': 0, 'name': "Root node", 'sub': []}
    }

    for p in data:
        # out.setdefault(p['parent_id'], {'sub': []})
        # out.setdefault(p['id'], {'sub': []})
        # setdefault的意思是如果key不存在则插入，若存在则返回此key对应的值
        if p['parent_id'] not in out:
            out[p['parent_id']] = {'sub': []}
        if p['id'] not in out:
            out[p['id']] = {'sub': []}
        out[p['id']].update(p)
        out[p['parent_id']]['sub'].append(out[p['id']])
        pprint('------------------------')
        pprint(out)

    return out[0]


tree = list_to_tree(data)

pprint(tree)

"""
mysql递归查询
父子查询： 根据父 id 查询下面所有子节点数据；
子父查询： 根据子 id 查询上面所有父节点数据 
                                    ————mysql递归查询


select T2.*
from
(
    select @r AS _id,
        (SELECT @r := p_id FROM table WHERE id = _id) AS p_id,
        @l := @l + 1 AS lvl
    from
    (select @r := 1, @l := 0) vars,
    table_name h
    where @r <> 0
) t1
join table_name t2 ON t1._id = t2.id
where type = 'continent'
order BY t1.lvl desc

"""
