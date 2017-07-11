// Delete notifications support
$('.notifications button.delete').click(function(){
	$(this).parent().remove();
});

// Hamburguer menu support
$('.navbar .navbar-burger').click(
function(){
	$(this).toggleClass('is-active');
	$('.navbar .navbar-menu').toggleClass('is-active');
});
