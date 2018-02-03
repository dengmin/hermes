define(['text!static/view/login.html'], function (tpl) {
    return {
        template: tpl,
        data: function(){
            return {
                username: '',
                password: '',
                isBtnLoading: false
            }
        },
        methods:{
            login: function(){
                var vm = this;
                if (!vm.username) {
                    vm.$message.error('请填写用户名！！！');
                    return;
                }
                if (!vm.password) {
                    vm.$message.error('请填写密码');
                    return;
                }
                var loginParams = {name: vm.username, password: vm.password};
                vm.isBtnLoading = true;
                vm.$router.push('/');
            }
        }
    }
});