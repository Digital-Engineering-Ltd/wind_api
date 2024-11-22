"""
Tests for models.
"""
from django.test import TestCase
from wind_assessments.models import WindAssessment
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.contrib.gis.geos import Point

# Create your tests here.


class WindAssessmentModelTests(TestCase):
    """Test Wind Assessment model."""

    def test_create_wind_assessment(self):
        """Test creating a wind assessment is successful."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123'
        )

        # Creating a wind assessment with the turbine type
        wind_assessment = WindAssessment.objects.create(
            user=user,
            customer_name='Test Customer',
            site_name='Test Site',
            report_type='feasibility',
            # lat=Decimal('35.12345'),
            # lon=Decimal('-120.12345'),
            # location='Test Location',
            position=Point(12.4924, 41.8902),
            turbine_type='turbine_model_a',
            date='2024-09-15',
            assessment_notes='Sample notes.'
        )

        self.assertEqual(
            str(wind_assessment),
            f"Wind Assessment for {wind_assessment.customer_name}"
        )
