jQuery(".multicolumn h3").each(
    function(el){
        $this = $(this);
		if (!$this.next("ul").length){ return; }
        var section = $this.wrap("<section>").parent();
        section.next("ul").appendTo(section);
    }
);
