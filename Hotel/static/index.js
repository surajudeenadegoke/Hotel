$(function(){
    $("#book_btn").click(function(){
        let room_booking = Number($("input[type='radio']:checked").attr('title'));
        let duration = Number($("#duration").val());
        $("#cost-of-booking").text(`$${room_booking * duration}`);
        $("#light-box").css("display","flex");
    })
    $("#pur_btn").click(function(){
        let sum = 0;
        $("input[type='checkbox']:checked").each(function(){
            sum += Number($(this).val());
        });
        $("#cost-of-services").text(`$${sum}`);
        $("#light-box-1").css("display","flex");
    })
});