require.config({
    paths: {
        vue: '/static/js/vue',
        vue_router: "/static/js/vue-router.min",
        vue_resource: "/static/js/vue-resource.min",
        ELEMENT: "/static/js/element/index",
        text: "/static/js/text",
        editor: '/static/js/vue-html5-editor'
    },
    urlArgs: 'v=20180131'
});

require(['vue','vue_router', 'vue_resource','ELEMENT', 'editor'], function(Vue,VueRouter,VueResource,Elem, editor){
    Vue.config.silent = true;
    Vue.use(VueRouter);
    Vue.use(VueResource);
    Vue.use(Elem);
    Vue.use(editor);

    Vue.filter('cutword', function(text){
        if(text.length > 50){
            return text.substring(0, 50) + '...';
        }
    });

    var view = {
        Index: function (resolver) {
            require(['/static/comp/index.js'], resolver);
        },
        User: function (resolver) {
          require(['/static/comp/users.js'], resolver);
        },
        Dept: function(resolver){
            require(['/static/comp/depts.js'], resolver);
        },
        Course: function (resolver) {
            require(['/static/comp/course.js'], resolver);
        },
        CourseEdit: function (resolver) {
            require(['/static/comp/course_edit.js'], resolver);
        },
        CourseStudent: function (resolver) {
            require(['/static/comp/course_student.js'], resolver);
        },
        NotFound: function (resolver) {
            require(['/static/comp/404.js'], resolver);
        }
    };

    var routes = [
        {
            path:'/',
            name: '首页',
            component: view.Index
        },
        {
            path: '/users',
            component: view.Index,
            name: '用户管理',
            children:[
                {path: '/users', name: '用户管理', component: view.User},
                {path: '/depts', name: '部门管理', component: view.Dept}
            ]
        },
        {
        path: '/course',
        name: '课程管理',
        component: view.Index,
        children:[
            {path: '/course', name: '课程管理', component: view.Course},
            {path: '/course/new',name:'新增课程', component: view.CourseEdit, meta:{action:'New'}},
            {path: '/course/edit/:course_id',name:'修改课程', component: view.CourseEdit, meta:{action:'Edit'}},
            {path: '/course/stds/:course_id', name: '课程学员列表', component: view.CourseStudent}
        ]},{
            path : '*',
            component: view.NotFound,
            hidden: true
        }];

    var router = new VueRouter({
        routes: routes
    });

   new Vue({
       router:router,
       delimiters: ['${', '}'],
       el: '#app'
    });


});