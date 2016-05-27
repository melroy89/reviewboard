from reviewboard.hostingsvcs.service import (register_hosting_service,
from reviewboard.testing.hosting_services import (SelfHostedTestService,
                                                  TestService)
    def test_ssh_disallowed(self):
        """Testing HgTool does not allow SSH URLs"""
        with self.assertRaises(SCMError):
            self.tool.check_repository('ssh://foo')


    def test_plain_repository(self):
        """Testing RepositoryForm with a plain repository"""
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'custom',
            'tool': self.git_tool_id,
            'path': '/path/to/test.git',
            'bug_tracker_type': 'none',
        })

        self.assertTrue(form.is_valid())

        repository = form.save()
        self.assertEqual(repository.name, 'test')
        self.assertEqual(repository.hosting_account, None)
        self.assertEqual(repository.extra_data, {})

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_plain_repository_with_missing_fields(self):
        """Testing RepositoryForm with a plain repository with missing fields
        """
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'custom',
            'tool': self.git_tool_id,
            'bug_tracker_type': 'none',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('path', form.errors)

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

            'test-hosting_account_username': 'testuser',
            'test-hosting_account_password': 'testpass',
        self.assertTrue(form.hosting_account_linked)
        self.assertEqual(repository.path, 'http://example.com/testrepo/')
        self.assertEqual(repository.mirror_path, '')

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_auth_error(self):
        """Testing RepositoryForm with a hosting service and new account and
        authorization error
        """
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'test-hosting_account_username': 'baduser',
            'test-hosting_account_password': 'testpass',
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertIn('hosting_account', form.errors)
        self.assertEqual(form.errors['hosting_account'],
                         ['Unable to link the account: The username is '
                          'very very bad.'])

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_2fa_code_required(self):
        """Testing RepositoryForm with a hosting service and new account and
        two-factor auth code required
        """
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'test-hosting_account_username': '2fa-user',
            'test-hosting_account_password': 'testpass',
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertIn('hosting_account', form.errors)
        self.assertEqual(form.errors['hosting_account'],
                         ['Enter your 2FA code.'])
        self.assertTrue(
            form.hosting_service_info['test']['needs_two_factor_auth_code'])

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_2fa_code_provided(self):
        """Testing RepositoryForm with a hosting service and new account and
        two-factor auth code provided
        """
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'test-hosting_account_username': '2fa-user',
            'test-hosting_account_password': 'testpass',
            'test-hosting_account_two_factor_auth_code': '123456',
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)
        self.assertFalse(
            form.hosting_service_info['test']['needs_two_factor_auth_code'])

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})

    def test_with_hosting_service_new_account_missing_fields(self):
        """Testing RepositoryForm with a hosting service and new account and
        missing fields
        """
        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)

        self.assertIn('hosting_account_username', form.errors)
        self.assertIn('hosting_account_password', form.errors)

        # Make sure the auth form also contains the errors.
        auth_form = form.hosting_auth_forms.pop('test')
        self.assertIn('hosting_account_username', auth_form.errors)
        self.assertIn('hosting_account_password', auth_form.errors)

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})
            'self_hosted_test-hosting_url': 'https://myserver.com',
            'self_hosted_test-hosting_account_username': 'testuser',
            'self_hosted_test-hosting_account_password': 'testpass',
        self.assertTrue(form.hosting_account_linked)
                         'https://myserver.com')
                         'https://myserver.com')
        self.assertEqual(repository.path, 'https://myserver.com/myrepo/')
        self.assertEqual(repository.mirror_path, 'git@myserver.com:myrepo/')

        # Make sure none of the other auth forms are unhappy. That would be
        # an indicator that we're doing form processing and validation wrong.
        for auth_form in six.itervalues(form.hosting_auth_forms):
            self.assertEqual(auth_form.errors, {})
            'self_hosted_test-hosting_url': '',
            'self_hosted_test-hosting_account_username': 'testuser',
            'self_hosted_test-hosting_account_password': 'testpass',
        self.assertFalse(form.hosting_account_linked)
        form = RepositoryForm(
            {
                'name': 'test',
                'hosting_type': 'test',
                'test-hosting_account_username': 'testuser',
                'test-hosting_account_password': 'testpass',
                'tool': self.git_tool_id,
                'test_repo_name': 'testrepo',
                'bug_tracker_type': 'none',
                'local_site': local_site.pk,
            },
            local_site_name=local_site.name)
        self.assertTrue(form.hosting_account_linked)
        account.data['password'] = 'testpass'
        account.save()
        self.assertFalse(form.hosting_account_linked)
    def test_with_hosting_service_existing_account_needs_reauth(self):
        """Testing RepositoryForm with a hosting service and existing
        account needing re-authorization
        """
        # We won't be setting the password, so that is_authorized() will
        # fail.
        account = HostingServiceAccount.objects.create(username='testuser',
                                                       service_name='test')

        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'hosting_account': account.pk,
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)
        self.assertEqual(set(form.errors.keys()),
                         set(['hosting_account_username',
                              'hosting_account_password']))

    def test_with_hosting_service_existing_account_reauthing(self):
        """Testing RepositoryForm with a hosting service and existing
        account with re-authorizating
        """
        # We won't be setting the password, so that is_authorized() will
        # fail.
        account = HostingServiceAccount.objects.create(username='testuser',
                                                       service_name='test')

        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
            'hosting_account': account.pk,
            'test-hosting_account_username': 'testuser2',
            'test-hosting_account_password': 'testpass2',
            'tool': self.git_tool_id,
            'test_repo_name': 'testrepo',
            'bug_tracker_type': 'none',
        })

        self.assertTrue(form.is_valid())
        self.assertTrue(form.hosting_account_linked)

        account = HostingServiceAccount.objects.get(pk=account.pk)
        self.assertEqual(account.username, 'testuser2')
        self.assertEqual(account.data['password'], 'testpass2')

        account.data['password'] = 'testpass'
        account.save()
            'self_hosted_test-hosting_url': 'https://example.com',
        self.assertFalse(form.hosting_account_linked)
    def test_with_self_hosted_and_invalid_account_service(self):
        invalid existing account due to mismatched service type
        account.data['password'] = 'testpass'
        account.save()
            'hosting_type': 'test',
            'hosting_account': account.pk,
            'tool': self.git_tool_id,
            'test_repo_name': 'myrepo',
            'bug_tracker_type': 'none',
        })
        form.validate_repository = False

        self.assertFalse(form.is_valid())
        self.assertFalse(form.hosting_account_linked)

    def test_with_self_hosted_and_invalid_account_local_site(self):
        """Testing RepositoryForm with a self-hosted hosting service and
        invalid existing account due to mismatched Local Site
        """
        account = HostingServiceAccount.objects.create(
            username='testuser',
            service_name='self_hosted_test',
            hosting_url='https://example1.com',
            local_site=LocalSite.objects.create(name='test-site'))
        account.data['password'] = 'testpass'
        account.save()

        form = RepositoryForm({
            'name': 'test',
            'hosting_type': 'test',
        self.assertFalse(form.hosting_account_linked)
        account.data['password'] = 'testpass'
        account.save()
        account.data['password'] = 'testpass'
        account.save()
        account.data['password'] = 'testpass'
        account.save()
        account.data['password'] = 'testpass'
        account.save()
        account.data['password'] = 'testpass'
        account.save()
        account.data['password'] = 'testpass'
        account.save()