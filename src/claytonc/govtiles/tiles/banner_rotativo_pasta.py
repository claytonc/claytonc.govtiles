# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from brasil.gov.tiles import _ as _
from collective.cover.tiles.base import IPersistentCoverTile, PersistentCoverTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from plone.autoform import directives as form
from plone.memoize import view
from plone.namedfile.field import NamedBlobImage as NamedImage
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from plone.app.uuid.utils import uuidToObject
from plone.app.uuid.utils import uuidToCatalogBrain
from zope import schema
from zope.interface import implements


class IBannerRotativoPastaTile(IPersistentCoverTile):

    form.omitted('header')
    form.no_omit(IDefaultConfigureForm, 'header')
    header = schema.TextLine(
        title=_(u'Header'),
        required=False,
        readonly=True,
    )

    form.omitted('title')
    form.no_omit(IDefaultConfigureForm, 'title')
    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
        readonly=True,
    )

    form.omitted('description')
    form.no_omit(IDefaultConfigureForm, 'description')
    description = schema.Text(
        title=_(u'Description'),
        required=False,
        readonly=True,
    )

    form.omitted('date')
    form.no_omit(IDefaultConfigureForm, 'date')
    date = schema.Datetime(
        title=_(u'Date'),
        required=False,
        readonly=True,
    )

    form.omitted('image')
    form.no_omit(IDefaultConfigureForm, 'image')
    image = NamedImage(
        title=_(u'Image'),
        required=False,
        readonly=True,
    )

    size = schema.Choice(
        title=_(u'Number of items to display'),
        values=(2, 3, 4),
        default=3,
        required=True,
    )

    layout = schema.Choice(
        title=u'Layout',
        values=(u'Banner',
                u'Chamada de foto',
                u'Texto sobreposto'),
        default=u'Banner',
        required=True,
    )

    form.omitted('uuids')
    form.no_omit(IDefaultConfigureForm, 'uuids')
    uuids = schema.List(
        title=_(u'Elements'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


class BannerRotativoPastaTile(PersistentCoverTile):
    implements(IBannerRotativoPastaTile)

    index = ViewPageTemplateFile('templates/banner_rotativo_pasta.pt')
    is_configurable = True
    is_editable = True
    limit = 4

    @property
    def portal_catalog(self):
        return self.context.portal_catalog

    def populate_with_object(self, obj):
        super(BannerRotativoPastaTile, self).populate_with_object(obj)  # check permission
        uuid = IUUID(obj, None)
        data_mgr = ITileDataManager(self)
        data_mgr.set({'uuid': uuid})

    def thumbnail(self, item):
        """Return a thumbnail of an image if the item has an image field and
        the field is visible in the tile.

        :param item: [required]
        :type item: content object
        """
        if self._has_image_field(item):
            scales = item.restrictedTraverse('@@images')
            return scales.scale('image', width=750, height=423)

    @view.memoize
    def accepted_ct(self):
        return ['Folder']

    def layout_banner(self):
        if self.data['layout'] == u'Banner' or self.data['layout'] is None:
            layout = 1
        elif self.data['layout'] == u'Chamada de foto':
            layout = 2
        else:
            layout = 3

        return layout

    def show_description(self):
        return self.data['layout'] == u'Chamada de foto'

    def show_rights(self):
        return self.data['layout'] == u'Chamada de foto' or self.data['layout'] == u'Texto sobreposto'

    def tile_class(self):
        if self.layout_banner() == 1:
            return 'chamada_sem_foto tile-content'
        elif self.layout_banner() == 2:
            return 'chamada_com_foto tile-content'
        else:
            return 'chamada_sobrescrito tile-content'

    def show_nav(self):
        return len(self.results()) > 1

    def get_uuid_object(self):
        uuid = self.data.get('uuid', None)
        if uuid:
            return uuidToCatalogBrain(uuid)

    def results(self):
        """ Obtem a pasta para obter os filhos
        """
        pasta = self.get_uuid_object()
        contents = []

        if pasta:
            contents = self.obtem_external_content(pasta)

        return contents

    @view.memoize
    def obtem_external_content(self, pasta):
        """ Obtem os banner de um objeto pasta apartir de seu path na ordem
            que esta na pasta
        """

        result = []
        limit = self.data.get('size') and self.data.get('size') or self.limit

        brains = self.portal_catalog(portal_type="ExternalContent",
                                     path={'query': pasta.getPath(), 'depth': 1},
                                     sort_on='getObjPositionInParent',
                                     review_state='published',
                                     sort_limit=limit)[:limit]
        for brain in brains:
            if not brain.exclude_from_nav:
                uid = brain.UID
                obj = uuidToObject(uid)
                result.append(obj)
        return result

    def get_uid(self, obj):
        return IUUID(obj, None)
