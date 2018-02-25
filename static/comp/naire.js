define(['text!static/view/naire.html'], function (tpl) {
    return {
        template: tpl,
        data: function () {
          return {}
        },
        methods: {
            load: function(){

            },
            add: function(){
                this.$router.push('/naire/create');
            }
        },
        mounted: function () {
            this.load();
        }
    }
});