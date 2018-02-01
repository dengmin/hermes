define(['text!static/view/users.html'], function (tpl) {
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
               this.$http.get('/user/list', {params:params}).then(function(res){
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
           }
       },
       mounted:function(){
           this.load();
       }
   }
});