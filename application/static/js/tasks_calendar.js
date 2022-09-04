$('document').ready(function() {
      
    /* initialize the external events
    -----------------------------------------------------------------*/

    // var containerEl = document.getElementById('external-events-list');
    // new FullCalendar.Draggable(containerEl, {
    //   itemSelector: '.fc-event',
    //   eventData: function(eventEl) {
    //     return {
    //       title: eventEl.innerText.trim()
    //     }
    //   }
    // });


    /* initialize the calendar
    -----------------------------------------------------------------*/

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,listWeek'
      },
      firstDay: 1,
      displayEventEnd: true,
      visibleRange: function(currentDate) {
        var startDate = new Date(currentDate.valueOf());
        var endDate = new Date(currentDate.valueOf());
    
        // Adjust the start & end dates, respectively
        startDate.setDate(startDate.getDate() - 1); // One day in the past
        endDate.setDate(endDate.getDate() + 2); // Two days into the future
    
        return { start: startDate, end: endDate };
      },
      eventClick: function(info) {
        // alert('Event: ' + info.event.id);
        $t = $(info.el);
        prcl = '';
        prcl2 = '';
        prtxt = '';
        if ($t.hasClass('priority-3')) {
          prcl = 'bg-danger text-light';
          prcl2 = 'border-danger';
          prtxt = 'Urgent';
        } else if ($t.hasClass('priority-2')) {
          prcl = 'bg-warning';
          prcl2 = 'border-warning';
          prtxt = 'High priority';
        } else if ($t.hasClass('priority-1')) {
          prcl = 'bg-info';
          prcl2 = 'border-info';
          prtxt = 'Medium priority';
        } else {
          prcl = 'bg-light';
          prcl2 = 'd-none';
        }
        $('#viewModal .modal-header').addClass(prcl).find('h5').text($t.text());
        $('#viewModal .task-priority').addClass(prcl2).text(prtxt);
        new bootstrap.Modal('#viewModal').show();
      },
      events: [
        {
          id: 111,
          title: 'A long completed task',
          start: '2022-06-22',
          end: '2022-07-05',
          className: 'completed'
        },
        {
          id: 122,
          title: 'A low priority task',
          start: '2022-07-04',
          end: '2022-07-09',
          className: 'priority-0'
        },
        {
          id: 118,
          title: 'An high priority task with a long title to see what it does in the calendar view',
          start: '2022-07-12',
          end: '2022-07-12',
          className: 'priority-2'
        },
        {
          id: 129,
          title: 'An urgent task',
          start: '2022-07-28',
          end: '2022-07-29',
          className: 'priority-3'
        },
        {
          id: 132,
          title: 'A normal priority 2-days task',
          start: '2022-07-28',
          end: '2022-07-30', // end dates are exclusive
          className: 'priority-1'
        }
      ],
      height: 'auto',
      editable: true,
      droppable: true, // this allows things to be dropped onto the calendar
      drop: function(arg) {
        console.log('Dropped event #'+arg.draggedEl.dataset.id+' on '+arg.dateStr);
        // is the "remove after drop" checkbox checked?
        if (document.getElementById('drop-remove').checked) {
          // if so, remove the element from the "Draggable Events" list
          arg.draggedEl.parentNode.removeChild(arg.draggedEl);
        }
      },
      eventChange: function(arg) {
        console.log('Modified an event:', arg)
      }
    });
    calendar.render();

});