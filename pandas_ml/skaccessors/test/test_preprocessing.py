#!/usr/bin/env python

import numpy as np
import pandas as pd

import sklearn.datasets as datasets
import sklearn.preprocessing as pp

import pandas_ml as pdml
import pandas_ml.util.testing as tm


class TestPreprocessing(tm.TestCase):

    def test_objectmapper(self):
        df = pdml.ModelFrame([])
        self.assertIs(df.preprocessing.Binarizer, pp.Binarizer)
        self.assertIs(df.preprocessing.Imputer, pp.Imputer)
        self.assertIs(df.preprocessing.KernelCenterer, pp.KernelCenterer)
        self.assertIs(df.preprocessing.LabelBinarizer, pp.LabelBinarizer)
        self.assertIs(df.preprocessing.LabelEncoder, pp.LabelEncoder)
        self.assertIs(df.preprocessing.MultiLabelBinarizer, pp.MultiLabelBinarizer)
        self.assertIs(df.preprocessing.MinMaxScaler, pp.MinMaxScaler)
        self.assertIs(df.preprocessing.Normalizer, pp.Normalizer)
        self.assertIs(df.preprocessing.OneHotEncoder, pp.OneHotEncoder)
        self.assertIs(df.preprocessing.StandardScaler, pp.StandardScaler)
        self.assertIs(df.preprocessing.PolynomialFeatures, pp.PolynomialFeatures)

    def test_add_dummy_feature(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        result = df.preprocessing.add_dummy_feature()
        expected = pp.add_dummy_feature(iris.data)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)

        result = df.preprocessing.add_dummy_feature(value=2)
        expected = pp.add_dummy_feature(iris.data, value=2)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns[1:], df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, pdml.ModelSeries))
        result = s.preprocessing.add_dummy_feature()
        expected = pp.add_dummy_feature(iris.data[:, [0]])

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.columns[1], 'sepal length (cm)')

    def test_binarize(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        result = df.preprocessing.binarize()
        expected = pp.binarize(iris.data)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        result = df.preprocessing.binarize(threshold=5)
        expected = pp.binarize(iris.data, threshold=5)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, pdml.ModelSeries))
        result = s.preprocessing.binarize()
        expected = pp.binarize(iris.data[:, 0])[0]

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

        result = s.preprocessing.binarize(threshold=6)
        expected = pp.binarize(iris.data[:, 0], threshold=6)[0]

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_normalize(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        result = df.preprocessing.normalize()
        expected = pp.normalize(iris.data)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, pdml.ModelSeries))
        result = s.preprocessing.normalize()
        expected = pp.normalize(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_normalize_abbr(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        result = df.pp.normalize()
        expected = pp.normalize(iris.data)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, pdml.ModelSeries))
        result = s.pp.normalize()
        expected = pp.normalize(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_scale(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        result = df.preprocessing.scale()
        expected = pp.scale(iris.data)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.data.values, expected)
        self.assert_index_equal(result.columns, df.data.columns)

        s = df['sepal length (cm)']
        self.assertTrue(isinstance(s, pdml.ModelSeries))
        result = s.preprocessing.scale()
        expected = pp.scale(np.atleast_2d(iris.data[:, 0]))[0]

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assertEqual(result.name, 'sepal length (cm)')

    def test_preprocessing_assignment(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        original_columns = df.data.columns
        df['sepal length (cm)'] = df['sepal length (cm)'].preprocessing.binarize(threshold=6)
        self.assertTrue(isinstance(df, pdml.ModelFrame))
        binarized = pp.binarize(np.atleast_2d(iris.data[:, 0]), threshold=6)
        expected = np.hstack([binarized.T, iris.data[:, 1:]])
        self.assert_numpy_array_almost_equal(df.data.values, expected)
        self.assert_index_equal(df.data.columns, original_columns)

        # recreate data
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        target_columns = ['sepal length (cm)', 'sepal width (cm)']
        df[target_columns] = df[target_columns].preprocessing.binarize(threshold=6)
        self.assertTrue(isinstance(df, pdml.ModelFrame))
        binarized = pp.binarize(iris.data[:, 0:2], threshold=6)
        expected = np.hstack([binarized, iris.data[:, 2:]])
        self.assert_numpy_array_almost_equal(df.data.values, expected)
        self.assert_index_equal(df.data.columns, original_columns)

    def test_transform(self):
        iris = datasets.load_iris()
        df = pdml.ModelFrame(iris)

        models = ['Binarizer', 'Imputer', 'Normalizer',
                  'StandardScaler', 'MinMaxScaler']
        for model in models:
            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            df.fit(mod1)
            mod2.fit(iris.data, iris.target)

            result = df.transform(mod1)
            expected = mod2.transform(iris.data)

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_series_equal(df.target, result.target)
            self.assert_numpy_array_almost_equal(result.data.values, expected)
            self.assert_index_equal(result.columns, df.columns)

            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = df.fit_transform(mod1)
            expected = mod2.fit_transform(iris.data)

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_series_equal(df.target, result.target)
            self.assert_numpy_array_almost_equal(result.data.values, expected)
            self.assert_index_equal(result.columns, df.columns)

    def test_transform_1d_frame_int(self):
        arr = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
        idx = pd.Index('a b c d e f g h i'.split(' '))
        df = pdml.ModelFrame(arr, index=idx, columns=['X'])
        self.assertEqual(len(df.columns), 1)

        if pd.compat.PY3:
            models = ['Binarizer', 'Imputer', 'StandardScaler']
            # MinMaxScalar raises TypeError in ufunc
        else:
            models = ['Binarizer', 'Imputer', 'StandardScaler', 'MinMaxScaler']

        for model in models:
            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            df.fit(mod1)
            mod2.fit(arr)

            result = df.transform(mod1)
            expected = mod2.transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_numpy_array_almost_equal(result.values.flatten(), expected)
            self.assert_index_equal(result.index, idx)
            self.assert_index_equal(result.columns, pd.Index(['X']))

            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = df.fit_transform(mod1)
            expected = mod2.fit_transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_numpy_array_almost_equal(result.values.flatten(), expected)
            self.assert_index_equal(result.index, idx)
            self.assert_index_equal(result.columns, pd.Index(['X']))

    def test_transform_1d_frame_float(self):
        arr = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3], dtype=np.float)
        idx = pd.Index('a b c d e f g h i'.split(' '))
        df = pdml.ModelFrame(arr, index=idx, columns=['X'])
        self.assertEqual(len(df.columns), 1)

        models = ['Binarizer', 'Imputer', 'StandardScaler', 'MinMaxScaler']
        for model in models:
            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            df.fit(mod1)
            mod2.fit(arr)

            result = df.transform(mod1)
            expected = mod2.transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_numpy_array_almost_equal(result.values.flatten(), expected)
            self.assert_index_equal(result.index, idx)
            self.assert_index_equal(result.columns, pd.Index(['X']))

            mod1 = getattr(df.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = df.fit_transform(mod1)
            expected = mod2.fit_transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelFrame))
            self.assert_numpy_array_almost_equal(result.values.flatten(), expected)
            self.assert_index_equal(result.index, idx)
            self.assert_index_equal(result.columns, pd.Index(['X']))

    def test_transform_series_int(self):
        arr = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3])
        s = pdml.ModelSeries(arr, index='a b c d e f g h i'.split(' '))

        if pd.compat.PY3:
            models = ['Binarizer', 'Imputer', 'StandardScaler']
            # MinMaxScalar raises TypeError in ufunc
        else:
            models = ['Binarizer', 'Imputer', 'StandardScaler', 'MinMaxScaler']

        for model in models:
            mod1 = getattr(s.preprocessing, model)()
            mod2 = getattr(pp, model)()

            s.fit(mod1)
            mod2.fit(arr)

            result = s.transform(mod1)
            expected = mod2.transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)

            mod1 = getattr(s.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = s.fit_transform(mod1)
            expected = mod2.fit_transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)

    def test_transform_series_float(self):
        arr = np.array([1, 2, 3, 1, 2, 3, 1, 2, 3], dtype=np.float)
        s = pdml.ModelSeries(arr, index='a b c d e f g h i'.split(' '))

        models = ['Binarizer', 'Imputer', 'StandardScaler', 'MinMaxScaler']
        for model in models:
            mod1 = getattr(s.preprocessing, model)()
            mod2 = getattr(pp, model)()

            s.fit(mod1)
            mod2.fit(arr)

            result = s.transform(mod1)
            expected = mod2.transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)

            mod1 = getattr(s.preprocessing, model)()
            mod2 = getattr(pp, model)()

            result = s.fit_transform(mod1)
            expected = mod2.fit_transform(arr).flatten()

            self.assertTrue(isinstance(result, pdml.ModelSeries))
            self.assert_numpy_array_almost_equal(result.values, expected)

    def test_Imputer(self):
        arr = np.array([1, np.nan, 3, 2])
        s = pdml.ModelSeries(arr)

        mod1 = s.pp.Imputer(axis=1)
        s.fit(mod1)
        result = s.transform(mod1)

        expected = np.array([1, 2, 3, 2])

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)

        mod1 = s.pp.Imputer(axis=1)
        result = s.fit_transform(mod1)

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)

    def test_LabelBinarizer(self):
        arr = np.array([1, 2, 3, 2])
        s = pdml.ModelSeries(arr, index=['a', 'b', 'c', 'd'])

        mod1 = s.pp.LabelBinarizer()
        s.fit(mod1)
        result = s.transform(mod1)

        expected = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 0]])

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assert_index_equal(result.index, pd.Index(['a', 'b', 'c', 'd']))

        mod1 = s.pp.LabelBinarizer()
        result = s.fit_transform(mod1)

        self.assertTrue(isinstance(result, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(result.values, expected)

        inversed = result.inverse_transform(mod1)
        self.assertTrue(isinstance(inversed, pdml.ModelFrame))
        self.assert_numpy_array_almost_equal(inversed.values.flatten(), arr)
        self.assert_index_equal(result.index, pd.Index(['a', 'b', 'c', 'd']))

    def test_LabelBinarizer2(self):
        arr = np.array(['X', 'Y', 'Z', 'X'])
        s = pdml.ModelSeries(arr)

        lb = s.preprocessing.LabelBinarizer()
        s.fit(lb)

        binarized = s.transform(lb)
        self.assertTrue(isinstance(binarized, pdml.ModelFrame))

        expected = pd.DataFrame({0: [1, 0, 0, 1], 1: [0, 1, 0, 0], 2: [0, 0, 1, 0]})
        self.assert_frame_equal(binarized, expected)

        df = pdml.ModelFrame(datasets.load_iris())
        df.target.fit(lb)
        binarized = df.target.transform(lb)

        expected = pd.DataFrame({0: [1] * 50 + [0] * 100,
                                 1: [0] * 50 + [1] * 50 + [0] * 50,
                                 2: [0] * 100 + [1] * 50})
        self.assert_frame_equal(binarized, expected)

        df = pdml.ModelFrame(datasets.load_iris())
        df.target.fit(lb)
        df.target = df.target.transform(lb)
        self.assertEqual(df.shape, (150, 7))
        self.assert_frame_equal(df.target, expected)

    def test_LabelEncoder(self):
        arr = np.array(['X', 'Y', 'Z', 'X'])
        s = pdml.ModelSeries(arr, index=['a', 'b', 'c', 'd'])

        mod1 = s.pp.LabelEncoder()
        s.fit(mod1)
        result = s.transform(mod1)

        expected = np.array([0, 1, 2, 0])

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)
        self.assert_index_equal(result.index, pd.Index(['a', 'b', 'c', 'd']))

        mod1 = s.pp.LabelEncoder()
        result = s.fit_transform(mod1)

        self.assertTrue(isinstance(result, pdml.ModelSeries))
        self.assert_numpy_array_almost_equal(result.values, expected)

        inversed = result.inverse_transform(mod1)
        self.assertTrue(isinstance(inversed, pdml.ModelSeries))
        self.assert_numpy_array_equal(inversed.values.flatten(), arr)
        self.assert_index_equal(result.index, pd.Index(['a', 'b', 'c', 'd']))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure'],
                   exit=False)
