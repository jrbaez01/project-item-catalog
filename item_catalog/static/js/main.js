// Delete notifications
console.log("Removing notification.");
$('.notifications button.delete').click(function(){
	$(this).parent().remove();
});
