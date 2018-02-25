define(['text!static/view/index.html'], function (tpl) {
   return {
       template: tpl,
       data:function(){
           var menus = [{
                name:'用户管理',
                id: 1,
                url: '/',
                iconCls: 'el-icon-menu',
                children:[{
                    name: '部门管理',
                    id: 2,
                    url: '/depts'
                },{
                    name: '用户管理',
                    id: 3,
                    url: '/users'
                }]
            },{
               name: '课程管理',
               id: 3,
               url : '/',
               iconCls: 'el-icon-document',
               children:[{
                   name: '课程管理',
                   id: 4,
                   url: '/course'
               },{
                   name: '我的问卷',
                   id: 5,
                   url: '/naires'
               }]
           }];
           return {
               'menus':menus
           }
       },
       methods: {
           logout: function(){
               var vm = this;
				vm.$confirm('确认退出吗?', '提示', {
					type: 'warning'
				}).then(function(){
				    //vm.$http.get('/account/logout');
                    vm.$router.push('/');
                }).catch(function (reason) {
                    vm.$router.push('/')
                });
           }
       }
   }
});