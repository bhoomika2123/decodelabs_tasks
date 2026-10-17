import tempfile
import unittest
from pathlib import Path
import pandas as pd
from recommender import RecommendationEngine, normalize_skill

class RecommendationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = RecommendationEngine()

    def test_top_three_sorted(self):
        result = self.engine.recommend(['Python', 'SQL', 'Machine Learning', 'Pandas'])
        self.assertTrue(result['success'])
        self.assertGreaterEqual(len(result['recommendations']), 1)
        scores = [r['similarity'] for r in result['recommendations']]
        self.assertEqual(scores, sorted(scores, reverse=True))
        self.assertTrue(all(0 <= score <= 1 for score in scores))

    def test_alias_and_case_normalization(self):
        self.assertEqual(normalize_skill('  ML  '), 'machine learning')
        self.assertEqual(normalize_skill('PYTHON'), 'python')

    def test_duplicates_removed(self):
        result = self.engine.recommend(['Python', 'python', 'SQL', 'Machine Learning'])
        self.assertEqual(len(result['selected_skills']), 3)

    def test_too_few_skills_rejected(self):
        with self.assertRaises(ValueError):
            self.engine.recommend(['Python', 'SQL'])

    def test_unknown_skills_reported(self):
        result = self.engine.recommend(['Python', 'SQL', 'Machine Learning', 'MadeUpThing'])
        self.assertIn('madeupthing', result['unrecognized_skills'])

    def test_missing_dataset(self):
        with self.assertRaises(FileNotFoundError):
            RecommendationEngine('/definitely/not/a/dataset.csv')

    def test_missing_values_are_handled(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'skills.csv'
            pd.DataFrame([{'job_role':'Example Role','required_skills':'Python, SQL, Machine Learning','description':None,'category':'Example'}]).to_csv(path,index=False)
            engine = RecommendationEngine(path)
            result = engine.recommend(['Python','SQL','Machine Learning'])
            self.assertEqual(result['recommendations'][0]['description'], '')

if __name__ == '__main__':
    unittest.main()
