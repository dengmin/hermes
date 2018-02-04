#!/usr/bin/env python
from flask import Blueprint, request
from core.models import Dept
__all__ = ['bp']

bp = Blueprint('dept', __name__)

@bp.route('/list')
def list_dept():
    page = request.args.get('page', 1, int)
    limit = request.args.get('pagesize', 20, int)
    k = request.args.get('k')
    pagable = request.args.get('pagable')
    query = Dept.query
    if k:
        query = query.filter(Dept.name.ilike('%{0}%'.format(k)))
    try:
        if pagable:
            depts = query.paginate(page=page, per_page=limit)
            return {'success':True, 'data': depts.items, 'total': depts.total}
        else:
            depts = query.all()
            return {'success':True, 'data': depts, 'total': len(depts)}
    except:
        return {'success': True, 'data':[], 'total':0}

