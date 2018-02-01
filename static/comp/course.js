define(['text!static/view/course.html'], function (tpl) {
   return {
       template: tpl,
       data:function(){
           return {
               keyword: '',
               items:[],
               startPage: 1,
               total: 0,
               pageSize: 15,
               pageSizes: [15, 20, 50, 100]
           }
       },
       methods:{
           load: function(){
               var self = this;
               var params = {
                   k: self.keyword,
                   pagesize: self.pageSize,
                   page: self.startPage
               };
               this.$http.get('/course/list', {params:params}).then(function(res){
                   self.items = res.body.data;
                   self.total = res.body.total;

               });
           },
           query:function(){
               this.load();
           },
           handleSizeChange:function(v){
               this.pageSize = v;
               this.load();
           },
           handleCurrentChange:function(v){
               this.startPage = v;
               this.load();
           },
           goCreateCourse: function () {
               this.$router.push('/course/new')
           },
           edit_course:function(course_id){
               this.$router.push('/course/edit/'+course_id);
           },
           list_student:function(course_id){
               this.$router.push('/course/stds/'+course_id);
           }
       },
       mounted:function(){
           this.load();
       }
   }
});