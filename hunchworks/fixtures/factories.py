from fixturefactory import BaseFactory, DjangoMixin
import random

from hunchworks.models import UserProfile, Connection, TranslationLanguage, Invitation, Hunch, PRIVACY_CHOICES, Location, Album, Evidence, Group, UserProfileGroup
from django.contrib.auth.models import User
from hunchworks import hunchworks_enums as enums

class Base(BaseFactory, DjangoMixin):
    """Base settings for all factories"""
    pass

class AlbumFactory(Base):
    model = Album

    def getparams(self):
        """Define default model parameters here. Return dict.
        (params can be overridden at time of instantiation)"""
        pk = self.getUnusedPk()
        name = "album %s" % pk
        return locals()

    def lastly(self):
        """Optional method to do things like
        create m2m connections after instantiation"""
        a = self.last_obj_created
        for x in range(15):
            a.evidences.add(self.getRandInst(Evidence))

class EvidenceFactory(Base):
    model = Evidence

    def getparams(self):
        pk = self.getUnusedPk()
        title = "title %s" % pk
        time_created = "2011-01-01"
        time_modified = "2011-06-06"
        description = "some description of evidence %s" % pk
        location = self.getRandInst(Location)
        creator = self.getRandInst(UserProfile)
        link = 'http://www.google.com'
        return locals()

class HunchFactory(Base):
    model = Hunch

    def getparams(self):
        pk = self.getUnusedPk()
        creator = self.getRandInst(UserProfile)
        time_created = "2011-01-01"
        time_modified = "2011-08-08"
        title = 'markov %s' % pk
        privacy = random.choice(PRIVACY_CHOICES)[0]
        location = self.getRandInst(Location)
        description = 'markov %s' % pk
        return locals()

class GroupFactory(BaseFactory, DjangoMixin):
    model = Group

    def getparams(self):
        pk = self.getUnusedPk()
        name = "Group with pk %s" % pk
        abbreviation = "Grp %s" % pk
        description = "Group description %s" % pk
        #logo = models.ImageField(verbose_name="Group picture", upload_to="group_images", blank=True, null=True)
        type = random.choice(enums.GroupType.GetChoices())[0]
        privacy = random.choice(PRIVACY_CHOICES)[0]
        location = self.getRandInst(Location)
        return locals()

class LocationFactory(Base):
    model = Location

    def getparams(self):
        pk = self.getUnusedPk()
        latitude = self.number()
        longitude = self.number()
        name = 'markov %s' % pk
        return locals()

    def number(self):
        return '%0.2f' % (random.randint(-360,360) + random.random())


class ConnectionFactory(Base):
    model = Connection

    def getparams(self):
        user_profile = self.getRandInst(UserProfile)
        other_user_profile = self.getRandInst(UserProfile)
        status = random.choice(enums.ConnectionStatus.GetChoices())[0]
        return locals()

class UserFactory(Base):
    model = User

    def getparams(self):
        """ Define parameters to create a new object with.
        Return dict"""
        pk = self.getUnusedPk()
        username = 'markov_%s' % pk
        return locals()

    def lastly(self):
        #set default password to be username
        a = self.last_obj_created
        a.set_password(self.username)
        a.save()

class UserProfileGroupFactory(Base):
    model = UserProfileGroup

    def getparams(self):
        user_profile = self.getRandInst(UserProfile)
        group = self.getRandInst(Group)
        return locals()

class UserProfileFactory(Base):
    model = UserProfile

    def getparams(self):
        user = UserFactory().last_obj_created
        pk = user.pk
        title = random.choice(enums.UserTitle.GetChoices())[0]
        email = '%s@testhunchworks.com' % (user.username)
        privacy = random.choice(enums.PrivacyLevel.GetChoices())[0]

        ###blank = True for all below
        bio_text = "Soon to be markov text"
        phone = self.phonenumber()
        skype_name = "%s_onskype" % user.username
        website = self.website(user.username)
        #profile_picture = models.ImageField(upload_to="profile_images", blank=True)
        messenger_service = random.choice(enums.MessangerServices.GetChoices())[0]
        translation_language = self.getRandInst(TranslationLanguage)
        #invitation = self.getRandInst(Invitation)
        return locals()

    def lastly(self):
        #ConnectionFactory(uid1=pk, uid2=self.getRandInst(model=UserProfile).pk)
        #roles = Role
        #location_interests = Location

        #qualifications = Education
        #courses = Course
        pass

    def phonenumber(self):
        return  ''.join([str(random.randint(0,9))
                for x in range(random.choice([7,10,11,13,20]))])
    def website(self, subdomain):
        return  "%s%s%s" % (
                    random.choice(['www.','', 'http://', 'http://www.']),
                    subdomain,
                    random.choice(['.com', '.org', '.me', '.uk', '.it']))

