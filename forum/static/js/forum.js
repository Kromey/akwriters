$(function(){
	$('.dropdown-submenu a.dropdown-toggle').click(function(e){
		$(this).next('ul').toggle();
		$(this).next('ul').find('ul').hide();
		e.stopPropagation();
		e.preventDefault();
	});
});
