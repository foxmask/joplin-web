from rest_framework import serializers
from joplin_web.models import Folders, Notes, Tags, NoteTags


class FoldersSerializer(serializers.ModelSerializer):

    nb_notes = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Folders


class NotesSerializer(serializers.ModelSerializer):

    parent = FoldersSerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Folders.objects.using('joplin').all(),
                                                   source='folders',
                                                   write_only=True)

    def validate_title(self, value):
        """
        Check that the blog post is about Django.
        """
        if value == '':
            raise serializers.ValidationError("Title is empty")
        return value

    class Meta:
        fields = '__all__'
        model = Notes


class TagsSerializer(serializers.ModelSerializer):

    nb_notes = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Tags


class NoteTagsSerializer(serializers.ModelSerializer):

    note = NotesSerializer(read_only=True)
    tag = TagsSerializer(read_only=True)

    note_id = serializers.PrimaryKeyRelatedField(
        queryset=Notes.objects.using('joplin').all(), source='notes', write_only=True)
    tag_id = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.using('joplin').all(), source='tags', write_only=True)

    class Meta:
        fields = ('id', 'note_id', 'note', 'tag_id', 'tag', 'created_time',
                  'updated_time', 'user_created_time', 'user_updated_time',
                  'encryption_cipher_text', 'encryption_applied')
        model = NoteTags