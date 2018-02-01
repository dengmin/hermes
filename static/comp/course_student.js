define(['text!static/view/course_student.html'],function(tpl){
    return {
        template: tpl,
        data: function () {
            return {
                items: [],
                total: 0,
                pageSize: 20,
                page: 1,
                pageSizes: [15, 20, 50, 100]
            }
        },
        methods :{
            load: function(){
                var vm = this;
                var course_id = this.$route.params.course_id;
                var params={
                    page : vm.page,
                    pagesize : vm.pageSize
                };
                this.$http.get('/course/stds/'+course_id, {params:params}).then(function(res){
                    vm.total = res.body.total;
                    vm.items = res.body.items;
                });
            },
            handleSizeChange:function(v){
               this.pageSize = v;
               this.load();
            },
            handleCurrentChange:function(v){
               this.page = v;
               this.load();
            }
        },
        mounted:function(){
            this.load();
        }
    }
});