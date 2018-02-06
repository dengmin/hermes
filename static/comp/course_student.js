define(['text!static/view/course_student.html'],function(tpl){
    return {
        template: tpl,
        data: function () {
            return {
                dept_options:[],
                dept_id:'',
                username:'',
                uploadurl:'',
                course_id: '',
                user_id: '',
                items: [],
                total: 0,
                pageSize: 20,
                page: 1,
                pageSizes: [15, 20, 50, 100],
                dialogFormVisible:false,
                index: '',
                form: {
                    single: 0,
                    multi: 0,
                    judge: 0,
                    answer: 0,
                    makeup: '',
                    score: 0,
                    average: 0
                }
            }
        },
        methods :{
            load: function(){
                var vm = this;
                var params = {
                    page : vm.page,
                    pagesize : vm.pageSize,
                    dept_id: vm.dept_id,
                    username: vm.username
                };
                this.$http.get('/course/stds/'+vm.course_id, {params:params}).then(function(res){
                    vm.total = res.body.total;
                    vm.items = res.body.items;
                });
            },
            load_dept: function () {
                var vm = this;
                this.$http.get('/dept/list').then(function(res){
                    vm.dept_options = res.body.data;
                });
            },
            handleSizeChange:function(v){
               this.pageSize = v;
               this.load();
            },
            handleCurrentChange:function(v){
               this.page = v;
               this.load();
            },
            rowchange:function(e){
                console.log(e)
            },
            editScore: function(item, index){
                this.dialogFormVisible = true;
                this.form.single = item.single;
                this.form.multi = item.multi;
                this.form.judge = item.judge;
                this.form.answer = item.answer;
                this.form.makeup = item.makeup;
                this.user_id = item.user_id;
                this.index = index;
            },
            submitSocre: function () {
                var params = {
                    user_id: this.user_id,
                    single: this.form.single,
                    multi: this.form.multi,
                    judge: this.form.judge,
                    answer: this.form.answer,
                    makeup: this.form.makeup
                };
                var vm = this;
                this.$http.post('/course/score/'+this.course_id,params).then(function(res){
                    if(res.body.success){
                        vm.dialogFormVisible = false;
                        vm.load();
                    }
                }).catch(function(res){
                    vm.$message({message:res.body.message, type:'error'});
                });
            },
            on_upload:function(response){
                if(response.success){
                    this.load();
                }
            }
        },
        mounted:function(){
            this.course_id = this.$route.params.course_id;
            this.uploadurl = '/course/import/'+this.course_id;
            this.load();
            this.load_dept();
        }
    }
});