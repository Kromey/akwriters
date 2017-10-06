$(function(){
	$('.dropdown-submenu a.dropdown-toggle').click(function(e){
		$(this).next('ul').toggle();
		$(this).parent().toggleClass('submenu-open');
		e.stopPropagation();
		e.preventDefault();
	});
});
