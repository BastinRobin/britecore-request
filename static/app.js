(function ($) {
    $.fn.serializeFormJSON = function () {

        var o = {};
        var a = this.serializeArray();
        $.each(a, function () {
            if (o[this.name]) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        return o;
    };
})(jQuery);	
	
_.templateSettings.variable = 'item'; 

var template = _.template(
	$('.task').html()
);

var renderTasks = function(arr, el) {
$(el).html('');
	_.each(arr, function(elem) {
		$(el).prepend(template(elem));
	});
}

label = function(a) {
	
	switch(a) {
		case 'Billing':
			color = 'is-primary';

		case 'Policies':

			color = 'is-info';

		case 'Claims':

			color = 'is-warning';

		default:

			color = 'is-success';
	}

	return color;
}

up = function(id, client) {

  var data = {
    id: id,
    client: client,
    mode: 'up'
  };

  $.ajax({
      url: '/api/feature/priority',
      type: "POST",
      data: data,
      success: function(data) {
          
        data = _.sortBy(data, 'priority').reverse();

        renderTasks(data, '#'+client);

	    $.notify("Priority changed", "success");




      },
      error: function(err) {
        console.error(err);
      }
  });


}

down = function(id, client) {
	var data = {
	  id: id,
	  client: client,
	  mode: 'down'
	};

	$.ajax({
	    url: '/api/feature/priority',
	    type: "POST",
	    data: data,
	    success: function(data) {
	        
	      data = _.sortBy(data, 'priority').reverse();

	      renderTasks(data, '#'+client);

	      $.notify("Priority changed", "success");


	    },
	    error: function(err) {
	      console.error(err);
	    }
	});
}

$.ajax({
  url: '/api/feature',
  type: 'GET',
  success: function(data) {

  	// pick the total clients data
  	clients = _.groupBy(data, 'client');

  	// console.log(clients);
  	_.each(clients, function(d, index) {
  		
  		d = _.sortBy(d, 'priority').reverse();

    	renderTasks(d, '#'+index );
  	}) 

  },
  error: function(err) {
    console.error(err);
  }
});


$('.submit').on('click', function(e) {
	e.preventDefault();

	$.ajax({
	    url: '/api/feature',
	    type: "POST",
	    data: $('.feature-form').serializeFormJSON(),
	 
	    success: function(data) {
	    		
	    	data = _.sortBy(data, 'priority').reverse();

	      	renderTasks(data, '#'+data[0].client);

	      	$.notify("Task added", "success");


	    },
	    error: function(err) {
	      console.error(err);
	    }
	});

});