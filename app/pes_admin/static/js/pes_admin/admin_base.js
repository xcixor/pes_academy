$('#applicationsDropdown').on('click', function(){
    $('#hiddenApplicationActions').toggleClass('hidden ');
    $('#menuIdentifier').toggleClass('fa-angle-down fa-angle-up')
});

$('#applicationsDropdown li').click(function(e){
    e.stopPropagation();
});