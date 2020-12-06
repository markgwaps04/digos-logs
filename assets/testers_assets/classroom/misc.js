(function(jq) {
jq("button.reset-field").click(function() {
    const select = jq(this)
        .parents(".input-group")
        .find("select");

    select[0].selectedIndex = 0;

});
jq(".classrom_goto").change(function(e) {

    const field = jq(e.originalEvent.target);
    if(!field.is("[name=class_level]")) return;
    const section_goto = jq(".classrom_goto").find("#section_goto");
    const batch_goto = jq(".classrom_goto").find("#batch_goto");

    $form = jq(this).serialize_form();
    const type = jq(this).attr("typeof");

    const send = jq.ajax({
        url : "/"+type+"/classroom/goto",
        method: "get",
        data : $form,
        dataType : "json",
        beforeSend : function()
        {
            jq(".goto .overlay-spinner").addClass("show");

            section_goto
                .find("option")
                .not(".default")
                .remove();

            batch_goto
                .find("option")
                .not(".default")
                .remove();

        }
    });

    send.complete(function(){
        jq(".goto .overlay-spinner").removeClass("show");
    });

    send.done(function(result)
    {
        result.sections.forEach(function(per)
        {
            const option = jq("<option>");
            option.attr("value",per.id);
            option.html(String(per.name).capitalize());
            section_goto.append(option);
        });

        if(!result.sections.length) return;

        result.batch.forEach(function(per) {
            const option = jq("<option>");
            option.attr("value",per.id);
            option.html(String(per.name).capitalize());
            batch_goto.append(option);
        });

    })

});

jq(".classrom_goto").submit(function(e) {
    e.preventDefault();
    try {
        const $form = jq(this).serialize_form();
        const type = jq(this).attr("typeof");

        const class_level = $form.class_level || false;
        const section =$form.section || false;
        const batch = $form.batch || false;

        if(!class_level) return;

        const url = ["/",type];

        switch(true)
        {
            case class_level && !section && !batch:
                 url.push("/classroom/view?");
                 url.push("group=");
                 url.push(class_level);
                break;
            case class_level && section && !batch:
                 url.push("/section?");
                 url.push("section=");
                 url.push(section);
            default:
                 url.push("/batch?");
                 url.push("section=");
                 url.push(section);
                 url.push("&batch=");
                 url.push(batch);
                break;
        }

        window.location = url.join("");

    }catch(err)
    {
        console.log(err);
        debugger;
    }

});

jq('.icheck').iCheck({checkboxClass: 'icheckbox_square-green',radioClass: 'iradio_square-green'})



})(jQuery);
