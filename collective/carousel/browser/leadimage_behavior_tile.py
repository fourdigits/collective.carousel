from Acquisition import aq_inner
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.component import getUtility
from plone.app.contenttypes.behaviors.leadimage import ILeadImage


class LeadImageBehaviorTile(BrowserView):

    template = ViewPageTemplateFile('templates/lead_image_behavior_tile.pt')
    render = template

    def tag(self, scale='mini', css_class='tileImage'):
        """ return a tag for the leadimage"""
        context = aq_inner(self.context)
        leadimage = ILeadImage(context)
        field = leadimage.image
        if field is not None:
            if field.getSize() != 0:
                return context.unrestrictedTraverse('@@images').scale('image', width=200, height=200).tag(
                    css_class=css_class)

        # if getattr(context, 'tag', None) is not None:
        #     return context.tag(scale=scale, css_class=css_class)

        return ''

    def caption(self):
        context = aq_inner(self.context)
        field = context.getField(IMAGE_CAPTION_FIELD_NAME)
        if field is None:
            return ''

        return context.widget(IMAGE_CAPTION_FIELD_NAME, mode='view')

    def isAllowed(self):
        return True

    def modified(self):
    #     """http://svn.plone.org/svn/plone/Plone/trunk/Products/CMFPlone/browser/ploneview.py
    #     @return: Last modified as a string, local time format        """
    #     Get Plone helper view
    #     which we use to convert the date to local format
        plone = getMultiAdapter((self.context, self.request), name="plone")
        time = self.context.modified()
        return plone.toLocalizedTime(time)

    def published(self):
    #     """http://svn.plone.org/svn/plone/Plone/trunk/Products/CMFPlone/browser/ploneview.py
    #     @return: Last modified as a string, local time format        """
    #     Get Plone helper view
    #     which we use to convert the date to local format
        plone = getMultiAdapter((self.context, self.request), name="plone")
        time = self.context.effective()
        return plone.toLocalizedTime(time)

    def __call__(self):
        return self.render()
