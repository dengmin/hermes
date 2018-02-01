define(['text!static/view/course_edit.html'], function (tpl) {
   return {
       template: tpl,
       data:function(){
           var vm = this;
           var validators = {
               name:[
                   {required:true, message: '请输入课程名称', trigger: 'blur'}
               ],
               address:[
                   {required:true, message: '请输入培训地址', trigger: 'blur'}
               ],
               start_time: [
                {required: true, message: '请选择开始时间', trigger: 'change' }
              ],
              end_time: [
                { required: true, message: '请选择结束时间', trigger: 'change' }
              ]
           };
           var data = {
               action: this.$route.meta.action,
               validators: validators,
               activeName:'basic',
               postInProcess:false,
               form: {
                   name: '',
                   start_time:'',
                   end_time:'',
                   address: '',
                   category: 'other',
                   level:'junior',
                   train_type:'',
                   require:'',
                   obj:'',
                   exam_type:'',
                   students:'',
                   teachers:'',
                   share:'',
                   content:'',
                   remark:''
               },
               students:[],
               page: 1,
               pageSize:5,
               total: 0,
               pageSizes: [15, 20, 50, 100]
           };
           return data;
       },
       methods:{
           load: function(){
               var vm = this;
               if(vm.action === 'Edit'){
                   var course_id = vm.$route.params.course_id;
                   this.$http.get('/course/'+course_id).then(function(res){
                       vm.form = res.body.data;
                   });
                   vm.load_students();
               }
           },
           load_students:function(){
               var vm  = this;
               var course_id = vm.$route.params.course_id;
               var params = {
                   page : vm.page,
                   pagesize : vm.pageSize
               };
               this.$http.get('/course/stds/'+course_id, {params:params}).then(function(res){
                    vm.total = res.body.total;
                    vm.students = res.body.items;
                });
           },
           create:function () {
               var vm = this;
               this.$refs['form'].validate(function(valid){
                   console.log(valid);
                   if(valid){
                       vm.postInProcess = true;
                       var posturl = "/course/create";
                       if(vm.action === 'Edit'){
                           var course_id = vm.$route.params.course_id;
                           posturl = "/course/edit/"+ course_id;
                       }
                       vm.$http.post(posturl, vm.form).then(function(res){
                           vm.$message({message:'保存成功', type:'success'});
                           vm.postInProcess = false;
                           vm.$router.push('/course')
                       }, function () {
                           vm.postInProcess = false;
                       });
                   }else{
                       vm.$message({message:'填写有误, 请检查', type:'warning'});
                       return false;
                   }
               });
           },
           remark_change:function (val) {
               this.form.remark = val;
           },
           content_change:function(val){
               this.form.content = val;
           },
           share_change:function(val){
               this.form.share = val;
           },
           cancel:function () {
               this.$router.push('/course');
           },
           handleSizeChange:function(v){
               this.pageSize = v;
               this.load_students();
           },
           handleCurrentChange:function(v){
               this.page = v;
               this.load_students();
           }
       },
       mounted:function(){
            this.action = this.$route.meta.action;
            this.load();
       }
   }
});