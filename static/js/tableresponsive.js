jQuery(".block table").each(
    function(el){
        $this = $(this);
        $this.addClass('table table-condensed schedule-table');
        $this.wrap("<div class='row'><div class='col-sm-12'><div class='table-responsive'>").parent();
    }
);
