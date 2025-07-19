from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category, Company


class CategoryViewTests(APITestCase):
    def test_list(self):
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve(self):
        company = Company.objects.create(name="Test Company")
        category = Category.objects.create(company=company, name="Test Category")
        url = reverse("category-detail", args=[category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        company = Company.objects.create(name="Test Company")
        url = reverse("category-list")
        data = {"company": str(company.id), "name": "New Category"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update(self):
        company = Company.objects.create(name="Test Company")
        category = Category.objects.create(company=company, name="Test Category")
        url = reverse("category-detail", args=[category.id])
        data = {"company": str(company.id), "name": "Updated Category"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy(self):
        company = Company.objects.create(name="Test Company")
        category = Category.objects.create(company=company, name="Test Category")
        url = reverse("category-detail", args=[category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unique_constraint_same_company(self):
        company = Company.objects.create(name="Test Company")
        Category.objects.create(company=company, name="Duplicate Name")
        url = reverse("category-list")
        data = {"company": str(company.id), "name": "Duplicate Name"}
        response = self.client.post(url, data)
        # Should fail - same name in same company
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_same_name_different_companies(self):
        company1 = Company.objects.create(name="Company 1")
        company2 = Company.objects.create(name="Company 2")
        
        # Create category for company1
        Category.objects.create(company=company1, name="Technology")
        
        # Same name for company2 should be allowed
        url = reverse("category-list")
        data = {"company": str(company2.id), "name": "Technology"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_name_strip_spaces(self):
        company = Company.objects.create(name="Test Company")
        url = reverse("category-list")
        data = {"company": str(company.id), "name": "  Category Name  "}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Category Name")

    def test_fullwidth_to_halfwidth(self):
        company = Company.objects.create(name="Test Company")
        url = reverse("category-list")
        data = {"company": str(company.id), "name": "ＡＢＣ１２３　テスト"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "ABC123 テスト")
