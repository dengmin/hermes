#!/usr/bin/env python
from flask import Blueprint, request
from core.models import Naire

__all__ = ['bp']

bp = Blueprint('naire', __name__)

@bp.route('/list')
def naires():
    page = request.args.get('page', 1, int)
    limit = request.args.get('pagesize', 20, int)
    try:
        results = Naire.query.paginate(page=page, per_page=limit)
        return {'success': True, 'data': results.items, 'total': results.total}
    except:
        return {'success': True, 'data': [], 'total': 0}

@bp.route('/create', methods=['POST'])
def create_naire():
    pass