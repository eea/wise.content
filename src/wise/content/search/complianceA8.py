from collections import defaultdict

from wise.content.search import sql, db


DESCRIPTORS = {}


def register_descriptor(class_):
    DESCRIPTORS[class_.id] = class_

    return class_


@register_descriptor
class Descriptor5(object):
    title = 'D5 Eutrophication'
    id = title.split()[0]

    article8_mapper_classes = (
        # theme name / mapper class
        ('Nutrients', sql.MSFD8bNutrient),
    )


class Article8(object):
    def get_data_reported(self, marine_unit_id, descriptor):
        descriptor_class = DESCRIPTORS.get(descriptor, None)
        if not descriptor_class:
            return []

        res = []
        for mc in descriptor_class.article8_mapper_classes:
            theme_name = mc[0]
            mapper_class = mc[1]
            mc_assessment = getattr(sql, 'MSFD8b' + theme_name + 'Assesment')
            mc_assesment_ind = getattr(sql, 'MSFD8b' + theme_name + 'AssesmentIndicator')
            id_indicator_col = 'MSFD8b_' + theme_name + '_AssesmentIndicator_ID'
            # import pdb;pdb.set_trace()
            count, res = db.compliance_art8_join(
                [
                 # getattr(mc_assesment_ind, id_indicator_col),
                 mapper_class.Topic, mapper_class.Description, mapper_class.SumInfo1, mapper_class.SumInfo1Unit,
                 mapper_class.SumInfo1Confidence, mapper_class.TrendsRecent, mapper_class.TrendsFuture,
                 mc_assesment_ind.MSFD8b_Nutrients_AssesmentIndicator_ID,
                 mc_assesment_ind.GESIndicators, mc_assesment_ind.OtherIndicatorDescription,
                 mc_assesment_ind.ThresholdValue, mc_assesment_ind.ThresholdValueUnit,
                 mc_assesment_ind.ThresholdProportion, mc_assessment.Status, mc_assessment.StatusConfidence,
                 mc_assessment.StatusTrend, mc_assessment.StatusDescription, mc_assessment.Limitations,
                 mapper_class.RecentTimeStart, mapper_class.RecentTimeEnd
                 ],
                mc_assessment,
                mc_assesment_ind,
                mapper_class.MarineUnitID == marine_unit_id
            )

        return res

    def get_art8_crit_indics(self, art8data, criterion_labels):
        art8_crit_indics = defaultdict(list)
        if not art8data:
            return {}

        self.art8_columns = art8data[0].keys()

        for criterion in criterion_labels.keys():
            art8_crit_indics[criterion] = []

            for index, row in enumerate(art8data):
                # id_indicator = row[columns.index('MSFD8b_Nutrients_AssesmentIndicator_ID')]
                indicator = row[self.art8_columns.index('GESIndicators')]
                # import pdb;pdb.set_trace()
                if criterion == indicator:
                    art8_crit_indics[criterion].append(index)

            if not art8_crit_indics[criterion]:
                art8_crit_indics[criterion].append('')

        return art8_crit_indics

    def get_art8_col_span(self, art8_crit_indics):
        art8_colspan = len([item
                                 for sublist in art8_crit_indics.values()

                                 for item in sublist])

        return art8_colspan