define(['text!static/view/naire_edit.html'], function (tpl) {
    return {
        template: tpl,
        data: function () {
            var validators = {
               name:[
                   {required:true, message: '请输入问卷名称', trigger: 'blur'}
               ],
               comment:[
                   {required:true, message: '请输入问卷介绍', trigger: 'blur'}
               ],
               endtime: [
                 { required: true, message: '请选择截止时间', trigger: 'change' }
              ]
           };
            var data = {
                validators: validators,
                form:{
                    name: '',
                    comment:'',
                    endtime:''
                }
            };
          return data;
        },
        methods: {
            create: function(){
                var vm = this;
                this.$refs['naireform'].validate(function(valid){
                    if(valid){
                        vm.$router.push("/naires");
                    }else{
                        return false;
                    }
                });
            },
            cancel:function () {
                this.$router.push("/naires");
            }
        }
    }
});