
// USE STRICT
"use strict";

// UTC TIMESTAMP
var date_fmt = "MMM Do YYYY, H:mm:ss [UTC]";

// App Messages
var messages= {
			   "new_comment_prompt":"Are You Sure You Want To Add Comment To The Following Task ?",
			   "new_comment_success":"New Comment Created Successfully !",
			   "new_task_success":"New Task Created Successfully !",
			   "taskstatus_update":"Task Status Updated !",
			  };

try {

window.onload = function(){

// GET TASKS
 jQuery.ajax({
  url:'/get-task',
  method:'GET',
  dataType:'json',
  success:function(result){
  		var task_data ="";
	  	if(result){

	  		task_data +="<table>"
	  			
	  		jQuery.each(result.data, function(k,v){

	  			// console.log(v.fields);

	  			if (v.fields.Status==1){
	  			task_data +="<tr><span style='background-color:lightgreen;' ><td align='left' border-radius:15px;padding-left:10px;' >";
	  			task_data +='<input type="checkbox" id="'+v.pk+','+v.fields.Status+'" onclick=taskstatus_update(this.id) checked />';
	  			}
	  			else{
	  			task_data +="<tr><td align='left'>";
	  			task_data +='<input type=checkbox id="'+v.pk+','+v.fields.Status+'" onclick=taskstatus_update(this.id) />';
	  			}

	  			var status_flag ='';

	  			if(v.fields.Status==1){
	  			 status_flag = "<span style='margin-left:10px;background-color:lightgreen;font-size:12px;vertical-align:middle;border-radius:10px;padding:9px;' ><span style='color:black;' >Complete</span></span>";
	  			}
	  			
	  			task_data +='&nbsp;&nbsp;<label><a id='+v.pk+' href="javascript:" onclick="get_comments(this.id);" ><h2>'+v.fields.task_title+status_flag+'</h2></label></a>';
	  			
	  			task_data += "</td></span></tr>";

	        });
	        
	        task_data +="</table>";

	        var new_task_div = "<p align='left' style='margin-top:30px;' ><input type='button' class='btn btn-primary btn-md' value='Add New Task' data-toggle='modal' data-target='#task_modal' /></p>";

	        jQuery(".comment_container").append(task_data+new_task_div);

	    }

	  },
  error:function(err){

  	alert(err.statusText);
  	console.log(err);

  }

  });

}

}
catch(err){

	alert(err);
	console.log(err);
}


// GET COMMENTS
function get_comments(id)
{  
   try{

   		jQuery(".comment_box").html('');

   		var new_comment_div="";

   		jQuery(".comment_box").prepend(loader);

   		
   			jQuery.ajax({
				url:'/get-comment/'+id+'/',
				method:'GET',
				dataType:'json',
				success:function(result){
				var comment_data ="";
				var task_id = id;
				var loaded = 0;
				if(result){
	  			
	  			if(result.Status=='Fail'){alertify.error(result.Message);}
	  			
	  			jQuery.each(result.data, function(k,v){
	  			// console.log(v.fields);

	  			var comment_time = "<p style='margin-top:-40px;margin-left:160px;font-size:10px;' ><strong>"+moment(v.fields.task_timestamp).utc().format(date_fmt)+"</strong></p>";
	  			var comment = "<p style='padding:15px;text-align:left;'>"+v.fields.task_comment+"</p>";
	  			comment_data +='<div class="c_inlinebox" >'+comment_time+comment+'</div>';

	  			if(v.pk){loaded = 1;}
	  			
	  			});

				
	  			new_comment_div += "<p align='center' class='comment_div' ><textarea id='new_comment_"+id+"' style='width:300px;border-radius:10px;padding:10px;' placeholder='Enter New Comment' ></textarea></p><p style='margin-left:230px;' class='comment_div' ><input type=button class='btn-success btn-sm' value='Save' id='new_comment_"+id+"' onclick='new_comment(this.id)'/></p><br><strong id='default_err_comment' ></strong>";

	  			task_id = "";
		        			 	
				}
			
				if(loaded==0){setTimeout(function(){jQuery("#loader").fadeOut(1000);jQuery(".comment_box").prepend("<br><p class='comment_div' ><strong id='default_err_comment' >No Comments Found, Please Add Some Comments !</strong></p>")},1);}
				else if(loaded==1){setTimeout(function(){jQuery("#loader").fadeOut("slow");},1);}

				jQuery(".comment_box").append(comment_data+new_comment_div);

			  },
			  error:function(err){
			  	alert(err);
			  	console.log(err);
			  }

		  	});

   		

   }
   catch(err){
   	alert(err);
   	console.log(err);
   }
}

// NEW TASK
function new_task(){
	try{

		var task_val = jQuery("#new_task").val();
   		
	   	jQuery.ajax({
		  url:'/create-task?new_task='+task_val,
		  method:'POST',
		  success:function(result){
		   console.log(result);
		   if(result.Status=='Success'){
		   	alertify.success(messages.new_task_success);
		   	window.location.reload();
		   }
		   if(result.Status=='Fail'){alertify.error(result.Message);}
	  	  },
		  error:function(err){
		  	alert(err);
		  	console.log(err);
		  }

		});

		jQuery("#new_task").val('');

   }
   catch(err){
   	alert(err);
   	console.log(err);
   }
}

// NEW COMMENT
function new_comment(id){
	try{

		if(jQuery('#'+id).val().length>0){

			alertify.confirm(messages.new_comment_prompt, function () {

				var c_id = id.split('_')[2];
				var comment_val = jQuery("#"+id).val();
		   		var new_comment_data ='';
		   		
		   		// alert(comment_val);
			   	
			   	jQuery.ajax({
				  url:'/create-comment?c_id='+c_id+'&new_comment='+comment_val,
				  method:'POST',
				  success:function(result){
				   console.log(result);
				   if(result.Status=='Success'){
				   
				   	alertify.success(messages.new_comment_success);

				   	var new_comment_time = "<p style='margin-top:-40px;margin-left:160px;font-size:10px;' ><strong>"+moment(result.time_stamp).utc().format(date_fmt)+"</strong></p>";
		  		   	var new_comment = "<p style='padding:15px;text-align:left;'>"+comment_val+"</p>";
		  			new_comment_data +='<div class="c_inlinebox" >'+new_comment_time+new_comment+'</div>';

		  			if(jQuery('#default_err_comment').html().length>0){jQuery('#default_err_comment').html('');}
				   	jQuery(".comment_box").prepend(new_comment_data);
				   	jQuery("#new_comment").val('');

				   }
				   if(result.Status=='Fail'){alertify.error(result.Message);}

				   // window.location.reload();
			  	  },
				  error:function(err){
				  	alert(err);
				  	console.log(err);
				  }

				});

				jQuery('#modal_c_id').val('');
				jQuery("#"+id).val('');				

			});

	     }

   	}
   catch(err){
   	alert(err);
   	console.log(err);
   }
}


// Update Task
function taskstatus_update(v){
	try{

		var temp = v.split(',');
		var t_id = temp[0];
		var t_status = temp[1];
  		if(t_status=='false'){
  			t_status = 1;
  		}
  		else if(t_status=='true'){ 
  			t_status = 0;

  		}

	   	jQuery.ajax({
		  url:'/update-task?t_id='+t_id+'&t_status='+t_status,
		  method:'POST',
		  success:function(result){
		   console.log(result);
		   if(result.Status=='Success'){alertify.success(messages.taskstatus_update);}
		   if(result.Status=='Fail'){alertify.error(result.Message);}
		   setTimeout(function(){window.location.reload()},1000);
	  	  },
		  error:function(err){
		  	alert(err);
		  	console.log(err);
		  }

		});

   }
   catch(err){
   	alert(err);
   	console.log(err);
   }
}



