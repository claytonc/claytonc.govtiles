*****************
claytonc.govtiles
*****************

.. contents:: Conteúdo
   :depth: 2

Introdução
----------

Este pacote contem alguns tiles desenvolvidos para serem usados nos portais que utilizam o
portal Padrão do Governo Federal em Plone.

Instalação
----------

Para habilitar a instalação deste produto em um ambiente que utilize o
buildout:

1. Editar o arquivo buildout.cfg (ou outro arquivo de configuração) e
   adicionar o pacote ``claytonc.govtiles`` à lista de eggs da instalação::

        [buildout]
        ...
        eggs =
            claytonc.govtiles

2. Após alterar o arquivo de configuração é necessário executar
   ''bin/buildout -N'', que atualizará sua instalação.

3. Reinicie a instância do portal Plone.

4. Instale o produto por meio do painel de controle em **Complementos**.

5. Depois da instação por meio do do painel de controle em **Configurações da capa** na opção **Tiles disponíveis**
   procure por ''Banner Rotativo Pasta'' e ''Coleção em Colunas'' e habilite usando as setas.

