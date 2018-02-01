
# (code, msg, http_status_code)

NOT_FOUND = (1000, 'resource not found', 404)

USER_EXISTS = (2001, 'user already exists', 500)
USER_DUBLE_EAMIL = (2002, 'email address already exists', 500)
USER_PASSWD_ERROR = (2003, '两次的密码不一致', 500)
OLD_PASSWORD_ERROR = (2004, '原密码不正确', 500)
ROLE_NOT_BLANK = (2005, '角色名不能为空', 500)
ROLE_ALIAS_NOT_BLANK = (2006, 'alias不能为空', 500)
ROLE_EXISTS = (2007, '角色已经存在', 500)



SERVER_EXISTS = (3000, 'ip地址已经存在', 500)
SERVER_PASSWD_ERROR = (30001, 'server password error', 500)

APP_DEPLOYING = (4000, '当前的应用正在发布,暂时不能新建', 403)
APP_NOT_VERIFY = (4001, '应用不在等待验证状态', 500)