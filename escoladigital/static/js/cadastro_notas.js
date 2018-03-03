 $(document).ready(function(){
      
      $("#turma").change(function(){
        $("#bimestre, #tipo").val("");
        
        if($(this).children("option:selected").val() !== ""){        
          $("#divDisciplinas").load("/escola/serie/"+$(this).children("option:selected").attr("id-serie")+"/disciplinas/rendimento", function(){

              if(!($("#disciplinas").children('option:selected').length > 0)){
                
                $("#disciplinas").replaceWith("<label>Não existem disciplinas associadas.</label>");
              }
          });

          $("#bimestre, #tipo").parent().show();
        } else {
          $("#divDisciplinas").children().remove();
          $("#bimestre, #tipo").parent().hide();
          $(".alert").hide();
        }
      });


      $("#filtros").on('change','select.busca', function(){
        $(".alert").hide();
        $("#divAluno").children().remove();
          if(validarCamposBusca()){
            $("#divAluno").load("/rendimento/turma/"+$("#turma").val()+"/disciplina/"+$("#disciplinas").val()+"/bimestre/"+$("#bimestre").val()+"/tipo/"+$("#tipo").val(), function(){
              $("#divAluno").parent().show();
              $(".number").mask('00.0', {'reverse':true});
            });
          } else {
            $("#divAluno").append($("div[name=alert-busca]").clone().show())
          }

          //Se a turma selecionada for do Infantil, apenas a nota bimestral é mostrada
          if($("#turma option:selected").attr('modalidade') == "I"){
            $("#tipo").children().not('option[value=2]').hide();
          }else{
            $("#tipo").children().not('option[value=2]').show();
          }
          
      });

      $("#divAluno").on('click','#btn-salvar', function(){
          if(validarCamposValor()){
           var notas = []
            $("#divAluno table tbody tr").each(function(){
              var matricula = $(this).find(":hidden").val();
              var valor = $(this).find(':input[type=text]').val();
              if(!valor)
                valor = $(this).find('select').val();
              var disciplina = $("#disciplinas").val();
              var bimestre = $("#bimestre").val();
              var tipo = $("#tipo").val();

              var json = {
                  'matricula':parseInt(matricula),
                  'valor':parseFloat(valor),
                  'disciplina':parseInt(disciplina),
                  'bimestre':parseInt(bimestre),
                  'tipo':parseInt(tipo)
              } 

             notas.push(json);
            });

            atualizarNotasTurma(notas);
          }
      });

      $(".close").click(function(){
        $(this).parent().hide();
      });

});

//---------------Funções-------------------------
  function validarCamposValor(){
    let valid = true;
    $("input[name=valor], select[name=valor]").each(function(){

        if($(this).val() == ""){
          $("#alert-notas").show();
          valid = false;      
        }
    });
    return valid;
  };

  function validarCamposBusca(){
    let valid = true;

    $("select.busca").each(function(){
      if($(this).val()=="" || $("#disciplinas").length == 0){
        valid = false;
      }
    });

    return valid;
  }

  function atualizarNotasTurma(notas){
    $.ajax({
      type:'POST',
      headers: {'X-CSRFToken':$("input[name=csrfmiddlewaretoken]").val()},
      url:'/rendimento/notas/cadastrar',
      accept:'application/json',
      data:{'notas':JSON.stringify(notas)}
    }).done(function(response){
        if(response.sucess){
          $("#alert-success").show();
        }
    });
  }
