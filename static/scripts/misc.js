(function(jq) {

$.fn.form_modal = function(params) {

    const parent_form = jq(this);
    const spinner =  parent_form
        .closest(".modal")
        .find(".overlay-spinner");


    const data = parent_form.serialize_form();

    parent_form.submit(function(e) {
         e.preventDefault();
         continue_que = params.before(parent_form);

         const send = function() {

            const send_ajax = jq.ajax({
                url : parent_form.attr("action"),
                headers: {"X-CSRFToken": jq.cookie("csrftoken")},
                data : data,
                type : "post",
                beforeSend : function() {
                    spinner.addClass("show");
                },
                success : function() {
                    spinner.removeClass("show");
                },
                error : function(error_params) {
                    alert('Error occur please try again later');
                    console.log(error_params);
                }
             });

             send_ajax.done(function(res) {

                const $result = jq(res);

                params.after({
                    "$element" : parent_form,
                    "result" : res,
                    "$result" : $result
                });

               const is_modal = $result.is(".modal");

               if(!is_modal) return;
               $result.modal("show");

             });

         }

         if (typeof(continue_que) === "object" && continue_que.hasOwnProperty("options"))
         {
            continue_que.options.callback = function(value) {
                if(!value) return false;
                send();
            };

            return;
         }

         if((continue_que == false || false)) return false;
         send();
    });

    return parent_form;

};

})(jQuery);
