from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.
def upload_location(instance,filename):
    return "%s/%s" %(instance.id,filename)
class Post(models.Model):
    title =  models.CharField(max_length=150)
    slug  = models.SlugField(unique=True)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
    width_field =  models.IntegerField(default=0)
    height_field  = models.IntegerField(default=0)
    image  = models.ImageField(upload_to=upload_location,
             null=True,
             blank=True,
             width_field='width_field',
             height_field ='height_field')
    content  = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False,auto_now_add=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp  = models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return self.title
    
    def get_absoulte_url(self):
        return reverse("detail",kwargs={"slug":self.slug})

    def get_Update_absoulte_url(self):
        return reverse("Update",kwargs={"slug":self.slug})

    def get_Delete_absoulte_url(self):
        return reverse("delete",kwargs={"slug":self.slug})        

    class Meta:
        ordering = ["-timestamp","-update"]    

def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_post_receive(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receive,sender=Post)                         

