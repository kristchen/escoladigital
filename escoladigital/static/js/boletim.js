 $(document).ready(function(){
      
      $("#turma").change(function(){
        $("#divAluno").children().remove();
        $("#divAluno").load("/rendimento/turma/"+$("#turma").val()+"/boletim", function(){
          $("#divAluno").parent().show();
        });
        
      });

      $("#divAluno").on('click','#btn-emitir', function(){
        var alunos = [];
        $("#divAluno").find('input:checked').not('input[id=check-all]').each(function(){
          alunos.push(parseInt($(this).parent().prev(':hidden').val()));
        });
        emitirBoletim(alunos);
      });
      
      $("#divAluno").on('change','#check-all', function(){
        $(":checkbox").attr('checked', $(this).is(':checked'));
      });

      $(".close").click(function(){
        $(this).parent().hide();
      });


});

//---------------Funções-------------------------------------------------

function emitirBoletim(alunos){

  if(validarCampos()){
    $("#form").attr("action", '/rendimento/turma/'+$("#turma").val()+'/boletim/emitir');
    $("#alert").hide();
    $("#form").submit();

  }else{
    $("#alert").show();
  }
}

function validarCampos(){
  return $("#divAluno").find('input:checked').length > 0;
}