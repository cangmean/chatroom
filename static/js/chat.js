var vm = new Vue({
    el: '#app',
    data:{
        msg: '',
        ws: '',
    },
    ready:function(){
        this.ws = new WebSocket('ws://localhost:5000/chat');
    },
    methods:{
        echo: function(){
            if(!this.msg){
                return
            }
            this.ws.send(this.msg);
            this.msg = ''
            this.ws.onmessage = function(evt){
                var txt = document.createElement('p');
                txt.innerHTML = evt.data;
                $('.wind').append(txt)
            }
        }
    },
})
