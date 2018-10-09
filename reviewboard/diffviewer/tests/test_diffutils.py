from __future__ import unicode_literals
class GetDiffFilesTests(TestCase):
    @add_fixtures(['test_users', 'test_scmtools'])
    @add_fixtures(['test_users', 'test_scmtools'])
    @add_fixtures(['test_users', 'test_scmtools'])
    @add_fixtures(['test_users', 'test_scmtools'])
class GetOriginalFileTests(TestCase):
    fixtures = ['test_scmtools']
        parent_diff = (
            b'diff --git a/empty b/empty\n'
            b'new file mode 100644\n'
            b'index 0000000..e69de29\n'
            b'\n'
        diff = (
            b'diff --git a/empty b/empty\n'
            b'index e69de29..0e4b0c7 100644\n'
            b'--- a/empty\n'
            b'+++ a/empty\n'
            b'@@ -0,0 +1 @@\n'
            b'+abc123\n'
        )
        repository = self.create_repository(tool_name='Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(
            diffset=diffset,
            source_file='empty',
            source_revision=PRE_CREATION,
            dest_file='empty',
            dest_detail='0e4b0c7')
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()

        request_factory = RequestFactory()

        # 1 query for fetching the ``FileDiff.parent_diff_hash`` and 1 for
        # saving the object.
                request=request_factory.get('/'),
            .filter(pk=filediff.pk)
            .first()
                request=request_factory.get('/'),