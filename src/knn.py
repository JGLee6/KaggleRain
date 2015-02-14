from sklearn import neighbors
import loader
import condition_data
import integrator

dat = loader.load('data/train_subset.csv')
for k in dat:
    dat[k] = condition_data.substitute_nans(dat[k])
#cleaned_dict = loader.clean_dict(dat,  selectionFunc = loader.except_outlier_indices)

#fill in missing values
filled_dict = condition_data.attribute_expectations(dat)[0]

#integrated = integrator.integrate_all(cleaned_dict)
integrated = integrator.integrate_all(filled_dict)
