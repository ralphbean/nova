(function ( $ ) {
    var methods = {
        init : function( img_list ) 
        { 
            this.empty();
            this.removeData('state');
            var container = $("<ul class='img-box'></ul>");
            var inline_list = $("<ul class='img-box-sel'></ul>")
            $.each(img_list, function(i, v) {
                var ili = $("<img />").attr('src', "/imgsrv/"+v+"?size=m");
                var isi = $("<img />").attr('src', "/imgsrv/"+v+"?size=s");
                $("<li class='i-block'></li>").css({'display': 'none', 'z-index': i+4}).append(ili).appendTo(container);
                $("<li class='s-block'></li>").append(isi).appendTo(inline_list);
            });
            container.children("li").first().css('display', 'block');
            inline_list.children('li').first().addClass("ui-selected");
            container.appendTo(this);
            inline_list.appendTo(this);
            this.data('state', 0);

            this.img_box('rotate');
        },
        rotate : function()
        {
            var cont = this.find('.i-block');
            var sel_list = this.find('.s-block');

            var next_li, next_state, next_si;

            var curr_state = this.data('state');
            var curr_li = cont[curr_state];
            var curr_si = sel_list[curr_state];

            if (curr_state == cont.length-1)
            {
                next_li = cont[0];
                next_si = sel_list[0];
                next_state = 0;
            }
            else
            {
                next_li = cont[curr_state+1];
                next_si = sel_list[curr_state+1];
                next_state = curr_state+1;
            }

            this.data('state', next_state);
            $(next_li).addClass('img-box-fade');
            $(curr_li).addClass('img-box-fade');
        
            var ok = false;
            $('.img-box-fade').delay(3000).fadeToggle(1000, 'linear', function() {
                $('.img-box-fade').removeClass('img-box-fade');
                if (!ok) {
                     $(next_si).addClass('ui-selected');
                    $(curr_si).removeClass('ui-selected');
                    $(this).parent().parent().img_box('rotate');
                    ok = true;
                }
            });
        }
    }

    $.fn.img_box = function(method) {
        // Method calling logic
        if ( methods[method] ) {
            return methods[ method ].apply( this, Array.prototype.slice.call( arguments, 1 ));
        } else if ( typeof method === 'object' || ! method ) {
            return methods.init.apply( this, arguments );
        } else {
            $.error( 'Method ' +  method + ' does not exist on jQuery.img_box' );
        } 
     };

})(jQuery)
