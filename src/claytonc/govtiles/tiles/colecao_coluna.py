# -*- coding: utf-8 -*-
from collections import OrderedDict

from claytonc.govtiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from collective.cover.tiles.collection import CollectionTile
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from plone.tiles.interfaces import ITileDataManager
from plone.batching import Batch
from plone.directives import form
from plone.memoize import view
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class IColecaoColunaTile(IPersistentCoverTile):

    header = schema.TextLine(
        title=_(u'Cabeçalho'),
        required=False,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Titulo'),
        required=False,
    )

    footer = schema.TextLine(
        title=_(u'Rodapé'),
        required=False,
    )

    uuid = schema.TextLine(
        title=_(u'UUID'),
        readonly=True,
    )

    form.omitted(IDefaultConfigureForm, 'number_colunm')
    number_colunm = schema.Choice(
        title=_(u'Número de colunas'),
        vocabulary=SimpleVocabulary.fromValues([u'1', u'2', u'3']),
        required=True,
    )

    form.omitted(IDefaultConfigureForm, 'number_per_colunmn')
    number_per_colunmn = schema.Int(
        title=_(u'Número de itens por coluna'),
        required=True,
        default=5,
    )


class ColecaoColunaTile(CollectionTile):

    index = ViewPageTemplateFile('templates/colecao.pt')

    is_configurable = True
    is_editable = True
    configured_fields = OrderedDict()
    short_name = _(u'msg_short_name_colecao_coluna', default=u'Coleção em coluna')

    def populate_with_object(self, obj):
        super(ColecaoColunaTile, self).populate_with_object(obj)  # check permission

        if obj.portal_type in self.accepted_ct():
            header = safe_unicode(obj.Title())  # use collection's title as header
            footer = _(u'Mais…')
            uuid = IUUID(obj)

            data_mgr = ITileDataManager(self)
            data_mgr.set({
                'header': header,
                'footer': footer,
                'uuid': uuid,
            })

    def results(self):
        self.configured_fields = self.get_configured_fields()

        size_conf = self.data['number_per_colunmn']
        if size_conf:
            size = int(size_conf)
        else:
            size = 5

        colunm_conf = self.data['number_colunm']
        if colunm_conf:
            colunm = int(colunm_conf)
        else:
            colunm = 1

        uuid = self.data.get('uuid', None)
        obj = uuidToObject(uuid)

        if uuid and obj:
            htmlconf = [i.get('htmltag', 'h1') for i in self.configured_fields if i['id'] == 'title']
            if htmlconf:
                htmlconf = htmlconf[0]

            return self.obtem_paginacao(obj, size, colunm, htmlconf)

        else:
            self.remove_relation()
            return []

    @view.memoize
    def obtem_paginacao(self, obj, size, colunm, htmlconf):
        """ Obtem a paginação conforme as configurações do tile.
        """

        obj_results = obj.results(batch=False)
        if obj_results:
            batch = Batch.fromPagenumber(items=obj_results, pagesize=size, pagenumber=1, navlistsize=colunm)

            if colunm > 1:
                lista = []
                for nav in batch.navlist:
                    batch.pagenumber = nav
                    lista.append(list(batch))
                return {'colunm': colunm, 'itens': lista, 'htmlconf': htmlconf}
            else:
                return {'colunm': colunm, 'itens': [batch], 'htmlconf': htmlconf}
        else:
            return None

    def show_header(self):
        return self._field_is_visible('header')
