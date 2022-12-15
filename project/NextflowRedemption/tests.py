from django.test import TestCase
from django.urls import reverse
from NextflowRedemption import models
from django.test.client import RequestFactory

class PipelineTestCase(TestCase):
	def setUp(self):
		models.Pipeline.objects.create(
			name = "pipe",
			status = "finished",
			log = "blah",
			pipeline_path = "c:/",
			pipeline_config = "omaewamoushindeiru",
			pipleline_parameters = "nani",
			location = "A"
		)
		models.Template.objects.create(
			name = "temp",
			template_path = "X:/Monty",
			template_config = "X:/Python"
		)
		self.factory = RequestFactory()
	
	def test_pipelines(self):
		pipeline = models.Pipeline.objects.get(name="pipe")
		self.assertEqual(pipeline.status, "finished")

	def test_templates(self):
		template = models.Template.objects.get(template_path = "X:/Monty")
		self.assertEqual(template.name, "temp")

	def test_index(self):
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)

	def test_configDelete(self):
		response = self.client.get(reverse('configEdit', args=[1]))
		self.assertEqual(response.status_code, 200)

	def test_config(self):
		repsonse = self.client.get(reverse('config'))
		self.assertEqual(repsonse.status_code, 200)

	