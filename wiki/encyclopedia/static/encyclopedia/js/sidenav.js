function openNav() {
    closeNav_lang()
    document.getElementById('mysidenav').style.right = '0px';		
}
function closeNav() {
	document.getElementById('mysidenav').style.right = '-250px';
}

function openNav_lang() {
    closeNav()
    document.getElementById('langsidenav').style.right = '0px';
}
function closeNav_lang() {
	document.getElementById('langsidenav').style.right = '-250px';
}