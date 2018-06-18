# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, Numeric, Table, Unicode, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mssql.base import BIT
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class ART10TargetsMarineUnit(Base):
    __tablename__ = 'ART10_Targets_MarineUnit'

    Id = Column(Integer, primary_key=True)
    MarineReportingUnit = Column(Unicode(50), nullable=False)
    IdReportedInformation = Column(ForeignKey(u'ReportedInformation.Id'), nullable=False)

    ReportedInformation = relationship(u'ReportedInformation')


class ART10TargetsProgressAssessment(Base):
    __tablename__ = 'ART10_Targets_ProgressAssessment'

    Id = Column(Integer, primary_key=True)
    Parameter = Column(Unicode(50), nullable=False)
    ParameterOther = Column(Unicode(250))
    Element = Column(Unicode(50))
    Element2 = Column(Unicode(50))
    TargetValue = Column(Float(53))
    ValueAchievedUpper = Column(Float(53))
    ValueAchievedLower = Column(Float(53))
    ValueUnit = Column(Unicode(50))
    ValueUnitOther = Column(Unicode(100))
    TargetStatus = Column(Unicode(50))
    AssessmentPeriod = Column(Unicode(9), nullable=False)
    Description = Column(Unicode(2500))
    IdTarget = Column(ForeignKey(u'ART10_Targets_Target.Id'), nullable=False)

    ART10_Targets_Target = relationship(u'ART10TargetsTarget')


class ART10TargetsTarget(Base):
    __tablename__ = 'ART10_Targets_Target'

    Id = Column(Integer, primary_key=True)
    TargetCode = Column(Unicode(50), nullable=False)
    Description = Column(Unicode(2500), nullable=False)
    TimeScale = Column(Unicode(6), nullable=False)
    UpdateDate = Column(Unicode(6), nullable=False)
    UpdateType = Column(Unicode(50), nullable=False)
    IdMarineUnit = Column(ForeignKey(u'ART10_Targets_MarineUnit.Id'), nullable=False)

    ART10_Targets_MarineUnit = relationship(u'ART10TargetsMarineUnit')


class ART10TargetsTargetFeature(Base):
    __tablename__ = 'ART10_Targets_Target_Feature'

    Feature = Column(Unicode(250), primary_key=True, nullable=False)
    IdTarget = Column(ForeignKey(u'ART10_Targets_Target.Id'), primary_key=True, nullable=False)

    ART10_Targets_Target = relationship(u'ART10TargetsTarget')


class ART10TargetsTargetGESComponent(Base):
    __tablename__ = 'ART10_Targets_Target_GESComponent'

    GESComponent = Column(Unicode(50), primary_key=True, nullable=False)
    IdTarget = Column(ForeignKey(u'ART10_Targets_Target.Id'), primary_key=True, nullable=False)

    ART10_Targets_Target = relationship(u'ART10TargetsTarget')


class ART8ESACostDegradation(Base):
    __tablename__ = 'ART8_ESA_CostDegradation'

    Id = Column(Integer, primary_key=True)
    Description = Column(Unicode(2500))
    Approach = Column(Unicode(100), nullable=False)
    Results = Column(Unicode(2500), nullable=False)
    CostDegradationType = Column(Unicode(50))
    IdFeature = Column(ForeignKey(u'ART8_ESA_Feature.Id'), nullable=False)

    ART8_ESA_Feature = relationship(u'ART8ESAFeature')


class ART8ESACostDegradationIndicator(Base):
    __tablename__ = 'ART8_ESA_CostDegradation_Indicator'

    IndicatorCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdCostDegradation = Column(ForeignKey(u'ART8_ESA_CostDegradation.Id'), primary_key=True, nullable=False)

    ART8_ESA_CostDegradation = relationship(u'ART8ESACostDegradation')


class ART8ESAFeature(Base):
    __tablename__ = 'ART8_ESA_Feature'

    Id = Column(Integer, primary_key=True)
    Feature = Column(Unicode(250), nullable=False)
    IdMarineUnit = Column(ForeignKey(u'ART8_ESA_MarineUnit.Id'), nullable=False)

    ART8_ESA_MarineUnit = relationship(u'ART8ESAMarineUnit')


class ART8ESAFeatureGESComponent(Base):
    __tablename__ = 'ART8_ESA_Feature_GESComponent'

    GESComponent = Column(Unicode(50), primary_key=True, nullable=False)
    IdFeature = Column(ForeignKey(u'ART8_ESA_Feature.Id'), primary_key=True, nullable=False)

    ART8_ESA_Feature = relationship(u'ART8ESAFeature')


class ART8ESAFeatureNACE(Base):
    __tablename__ = 'ART8_ESA_Feature_NACE'

    NACECode = Column(Unicode(4), primary_key=True, nullable=False)
    IdFeature = Column(ForeignKey(u'ART8_ESA_Feature.Id'), primary_key=True, nullable=False)

    ART8_ESA_Feature = relationship(u'ART8ESAFeature')


class ART8ESAMarineUnit(Base):
    __tablename__ = 'ART8_ESA_MarineUnit'

    Id = Column(Integer, primary_key=True)
    MarineReportingUnit = Column(Unicode(50), nullable=False)
    IdReportedInformation = Column(ForeignKey(u'ReportedInformation.Id'), nullable=False)

    ReportedInformation = relationship(u'ReportedInformation')


class ART8ESAUsesActivity(Base):
    __tablename__ = 'ART8_ESA_UsesActivities'

    Id = Column(Integer, primary_key=True)
    Description = Column(Unicode(2500))
    Employment = Column(Float(53))
    ProductionValue = Column(Float(53))
    ValueAdded = Column(Float(53))
    IdFeature = Column(ForeignKey(u'ART8_ESA_Feature.Id'), nullable=False)

    ART8_ESA_Feature = relationship(u'ART8ESAFeature')


class ART8ESAUsesActivitiesEcosystemService(Base):
    __tablename__ = 'ART8_ESA_UsesActivities_EcosystemService'

    EcosystemServiceCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdUsesActivities = Column(ForeignKey(u'ART8_ESA_UsesActivities.Id'), primary_key=True, nullable=False)

    ART8_ESA_UsesActivity = relationship(u'ART8ESAUsesActivity')


class ART8ESAUsesActivitiesIndicator(Base):
    __tablename__ = 'ART8_ESA_UsesActivities_Indicator'

    IndicatorCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdUsesActivities = Column(ForeignKey(u'ART8_ESA_UsesActivities.Id'), primary_key=True, nullable=False)

    ART8_ESA_UsesActivity = relationship(u'ART8ESAUsesActivity')


class ART8ESAUsesActivitiesPressure(Base):
    __tablename__ = 'ART8_ESA_UsesActivities_Pressure'

    PressureCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdUsesActivities = Column(ForeignKey(u'ART8_ESA_UsesActivities.Id'), primary_key=True, nullable=False)

    ART8_ESA_UsesActivity = relationship(u'ART8ESAUsesActivity')


class ART8GESCriteriaStatu(Base):
    __tablename__ = 'ART8_GES_CriteriaStatus'

    Id = Column(Integer, primary_key=True)
    Criteria = Column(Unicode(50), nullable=False)
    CriteriaStatus = Column(Unicode(50), nullable=False)
    DescriptionCriteria = Column(Unicode(2500))
    IdOverallStatus = Column(ForeignKey(u'ART8_GES_OverallStatus.Id'))
    IdElementStatus = Column(ForeignKey(u'ART8_GES_ElementStatus.Id'))

    ART8_GES_ElementStatu = relationship(u'ART8GESElementStatu')
    ART8_GES_OverallStatu = relationship(u'ART8GESOverallStatu')


class ART8GESCriteriaValue(Base):
    __tablename__ = 'ART8_GES_CriteriaValues'

    Id = Column(Integer, primary_key=True)
    Parameter = Column(Unicode(50), nullable=False)
    ParameterOther = Column(Unicode(250))
    ThresholdValueUpper = Column(Float(53))
    ThresholdValueLower = Column(Float(53))
    ThresholdQualitative = Column(Unicode(250))
    ThresholdValueSource = Column(Unicode(50))
    ThresholdValueSourceOther = Column(Unicode(250))
    ValueAchievedUpper = Column(Float(53))
    ValueAchievedLower = Column(Float(53))
    ValueUnit = Column(Unicode(50))
    ValueUnitOther = Column(Unicode(100))
    ProportionThresholdValue = Column(Float(53))
    ProportionThresholdValueUnit = Column(Unicode(50))
    ProportionValueAchieved = Column(Float(53))
    Trend = Column(Unicode(50), nullable=False)
    ParameterAchieved = Column(Unicode(50), nullable=False)
    DescriptionParameter = Column(Unicode(2500))
    IdCriteriaStatus = Column(ForeignKey(u'ART8_GES_CriteriaStatus.Id'), nullable=False)

    ART8_GES_CriteriaStatu = relationship(u'ART8GESCriteriaStatu')


class ART8GESCriteriaValuesIndicator(Base):
    __tablename__ = 'ART8_GES_CriteriaValues_Indicator'

    IndicatorCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdCriteriaValues = Column(ForeignKey(u'ART8_GES_CriteriaValues.Id'), primary_key=True, nullable=False)

    ART8_GES_CriteriaValue = relationship(u'ART8GESCriteriaValue')


class ART8GESElementStatu(Base):
    __tablename__ = 'ART8_GES_ElementStatus'

    Id = Column(Integer, primary_key=True)
    Element = Column(Unicode(250))
    Element2 = Column(Unicode(250))
    ElementSource = Column(Unicode(50))
    ElementCode = Column(Unicode(50))
    Element2Code = Column(Unicode(50))
    ElementCodeSource = Column(Unicode(50))
    Element2CodeSource = Column(Unicode(50))
    DescriptionElement = Column(Unicode(2500))
    ElementStatus = Column(Unicode(50))
    IdOverallStatus = Column(ForeignKey(u'ART8_GES_OverallStatus.Id'), nullable=False)

    ART8_GES_OverallStatu = relationship(u'ART8GESOverallStatu')


class ART8GESMarineUnit(Base):
    __tablename__ = 'ART8_GES_MarineUnit'

    Id = Column(Integer, primary_key=True)
    MarineReportingUnit = Column(Unicode(50), nullable=False)
    IdReportedInformation = Column(ForeignKey(u'ReportedInformation.Id'), nullable=False)

    ReportedInformation = relationship(u'ReportedInformation')


class ART8GESOverallStatu(Base):
    __tablename__ = 'ART8_GES_OverallStatus'

    Id = Column(Integer, primary_key=True)
    GESComponent = Column(Unicode(50), nullable=False)
    Feature = Column(Unicode(250), nullable=False)
    GESExtentAchieved = Column(Numeric(8, 5))
    GESExtentUnit = Column(Unicode(250))
    GESExtentThreshold = Column(Numeric(8, 5))
    GESAchieved = Column(Unicode(50), nullable=False)
    AssessmentsPeriod = Column(Unicode(9), nullable=False)
    DescriptionOverallStatus = Column(Unicode(2500))
    IntegrationRuleTypeCriteria = Column(Unicode(50))
    IntegrationRuleDescriptionCriteria = Column(Unicode(1000))
    IntegrationRuleDescriptionReferenceCriteria = Column(Unicode(250))
    IntegrationRuleTypeParameter = Column(Unicode(50))
    IntegrationRuleDescriptionParameter = Column(Unicode(1000))
    IntegrationRuleDescriptionReferenceParameter = Column(Unicode(250))
    IdMarineUnit = Column(ForeignKey(u'ART8_GES_MarineUnit.Id'), nullable=False)

    ART8_GES_MarineUnit = relationship(u'ART8GESMarineUnit')


class ART8GESOverallStatusFeature(Base):
    __tablename__ = 'ART8_GES_OverallStatus_Feature'

    Feature = Column(Unicode(250), primary_key=True, nullable=False)
    IdOverallStatus = Column(ForeignKey(u'ART8_GES_OverallStatus.Id'), primary_key=True, nullable=False)

    ART8_GES_OverallStatu = relationship(u'ART8GESOverallStatu')


class ART8GESOverallStatusPressure(Base):
    __tablename__ = 'ART8_GES_OverallStatus_Pressure'

    PressureCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdOverallStatus = Column(ForeignKey(u'ART8_GES_OverallStatus.Id'), primary_key=True, nullable=False)

    ART8_GES_OverallStatu = relationship(u'ART8GESOverallStatu')


class ART8GESOverallStatusTarget(Base):
    __tablename__ = 'ART8_GES_OverallStatus_Target'

    TargetCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdOverallStatus = Column(ForeignKey(u'ART8_GES_OverallStatus.Id'), primary_key=True, nullable=False)

    ART8_GES_OverallStatu = relationship(u'ART8GESOverallStatu')


class ART9GESGESComponent(Base):
    __tablename__ = 'ART9_GES_GESComponent'

    Id = Column(Integer, primary_key=True)
    GESComponent = Column(Unicode(50), nullable=False)
    JustificationDelay = Column(Unicode(1000))
    JustificationNonUse = Column(Unicode(1000))
    IdReportedInformation = Column(ForeignKey(u'ReportedInformation.Id'), nullable=False)

    ReportedInformation = relationship(u'ReportedInformation')


class ART9GESGESDetermination(Base):
    __tablename__ = 'ART9_GES_GESDetermination'

    Id = Column(Integer, primary_key=True)
    GESDescription = Column(Unicode(2500), nullable=False)
    DeterminationDate = Column(Unicode(6), nullable=False)
    UpdateType = Column(Unicode(50), nullable=False)
    IdGESComponent = Column(ForeignKey(u'ART9_GES_GESComponent.Id'), nullable=False)

    ART9_GES_GESComponent = relationship(u'ART9GESGESComponent')


class ART9GESGESDeterminationFeature(Base):
    __tablename__ = 'ART9_GES_GESDetermination_Feature'

    Id = Column(Integer, primary_key=True)
    Feature = Column(Unicode(50), nullable=False)
    IdGESDetermination = Column(ForeignKey(u'ART9_GES_GESDetermination.Id'), nullable=False)

    ART9_GES_GESDetermination = relationship(u'ART9GESGESDetermination')


class ART9GESMarineUnit(Base):
    __tablename__ = 'ART9_GES_MarineUnit'

    MarineReportingUnit = Column(Unicode(50), primary_key=True, nullable=False)
    IdGESDetermination = Column(ForeignKey(u'ART9_GES_GESDetermination.Id'), primary_key=True, nullable=False)

    ART9_GES_GESDetermination = relationship(u'ART9GESGESDetermination')


t_FMEJobController = Table(
    'FMEJobController', metadata,
    Column('ReportNetURL', Unicode(255), nullable=False),
    Column('FMEWorkspace', Unicode(255), nullable=False),
    Column('FMEJobID', Unicode(50), nullable=False),
    Column('TimeStarted', DateTime, nullable=False),
    Column('TimeFinished', DateTime),
    Column('Result', Unicode)
)


class IndicatorsDataset(Base):
    __tablename__ = 'Indicators_Dataset'

    Id = Column(Integer, primary_key=True)
    URL = Column(Unicode(250), nullable=False)
    MD_URL = Column(Unicode(250))
    IdIndicatorAssessment = Column(ForeignKey(u'Indicators_IndicatorAssessment.Id'), nullable=False)

    Indicators_IndicatorAssessment = relationship(u'IndicatorsIndicatorAssessment')


class IndicatorsFeatureFeature(Base):
    __tablename__ = 'Indicators_Feature_Feature'

    Feature = Column(Unicode(250), primary_key=True, nullable=False)
    IdGESComponent = Column(ForeignKey(u'Indicators_Feature_GESComponent.Id'), primary_key=True, nullable=False)

    Indicators_Feature_GESComponent = relationship(u'IndicatorsFeatureGESComponent')


class IndicatorsFeatureGESComponent(Base):
    __tablename__ = 'Indicators_Feature_GESComponent'

    Id = Column(Integer, primary_key=True)
    GESComponent = Column(Unicode(50), nullable=False)
    IdIndicatorAssessment = Column(ForeignKey(u'Indicators_IndicatorAssessment.Id'), nullable=False)

    Indicators_IndicatorAssessment = relationship(u'IndicatorsIndicatorAssessment')


class IndicatorsIndicatorAssessment(Base):
    __tablename__ = 'Indicators_IndicatorAssessment'

    Id = Column(Integer, primary_key=True)
    IndicatorCode = Column(Unicode(50), nullable=False)
    IndicatorTitle = Column(Unicode(250), nullable=False)
    IndicatorSource = Column(Unicode(50), nullable=False)
    IndicatorSourceOther = Column(Unicode(50))
    UniqueReference = Column(Unicode(250), nullable=False)
    DatasetVoidReason = Column(Unicode(100))
    IdReportedInformation = Column(ForeignKey(u'ReportedInformation.Id'), nullable=False)

    ReportedInformation = relationship(u'ReportedInformation')


class IndicatorsIndicatorAssessmentTarget(Base):
    __tablename__ = 'Indicators_IndicatorAssessment_Target'

    TargetCode = Column(Unicode(50), primary_key=True, nullable=False)
    IdIndicatorAssessment = Column(ForeignKey(u'Indicators_IndicatorAssessment.Id'), primary_key=True, nullable=False)

    Indicators_IndicatorAssessment = relationship(u'IndicatorsIndicatorAssessment')


class IndicatorsMarineUnit(Base):
    __tablename__ = 'Indicators_MarineUnit'

    MarineReportingUnit = Column(Unicode(50), primary_key=True, nullable=False)
    IdIndicatorAssessment = Column(ForeignKey(u'Indicators_IndicatorAssessment.Id'), primary_key=True, nullable=False)

    Indicators_IndicatorAssessment = relationship(u'IndicatorsIndicatorAssessment')


class LCountry(Base):
    __tablename__ = 'L_Countries'

    Code = Column(Unicode(2), primary_key=True)
    Country = Column(Unicode(50), nullable=False)


class LFeature(Base):
    __tablename__ = 'L_Features'

    Code = Column(Unicode(50), primary_key=True)
    Feature = Column(Unicode(200))
    Subject = Column(Unicode(250))
    Theme = Column(Unicode(250))
    Sub_theme = Column('Sub-theme', Unicode(250))


class LGESComponent(Base):
    __tablename__ = 'L_GESComponents'

    Code = Column(Unicode(10), primary_key=True)
    Description = Column(Unicode(100))
    GESComponent = Column(Unicode(15))
    Old = Column(BIT, nullable=False, server_default=text("((0))"))


class LIntegrationRule(Base):
    __tablename__ = 'L_IntegrationRules'

    Code = Column(Unicode(15), primary_key=True)
    Label = Column(Unicode(50))
    Type = Column(Unicode(50))
    Description = Column(Unicode(1000))


class LNACECode(Base):
    __tablename__ = 'L_NACECodes'

    Code = Column(Unicode(4), primary_key=True)
    Label = Column(Unicode(255))


class LParameter(Base):
    __tablename__ = 'L_Parameters'

    Code = Column(Unicode(10), primary_key=True)
    Description = Column(Unicode(150))


class LThresholdSource(Base):
    __tablename__ = 'L_ThresholdSources'

    Code = Column(Unicode(20), primary_key=True)
    Description = Column(Unicode(150))


class LUnit(Base):
    __tablename__ = 'L_Units'

    Notation = Column(Unicode(20), primary_key=True)
    Description = Column(Unicode(50))


class MarineReportingUnit(Base):
    __tablename__ = 'MarineReportingUnit'

    CountryCode = Column(Unicode(2), primary_key=True, nullable=False)
    MarineReportingUnitId = Column(Unicode(50), primary_key=True, nullable=False)


class ReportedInformation(Base):
    __tablename__ = 'ReportedInformation'

    Id = Column(Integer, primary_key=True)
    CountryCode = Column(Unicode(2), nullable=False)
    Schema = Column(Unicode(50), nullable=False)
    ContactMail = Column(Unicode(50), nullable=False)
    ContactName = Column(Unicode(100))
    ContactOrganisation = Column(Unicode(1000), nullable=False)
    ReportingDate = Column(Date, nullable=False)
    ReportedFileLink = Column(Unicode(350), nullable=False)
    IdReportingPeriod = Column(ForeignKey(u'ReportingPeriod.Id'), nullable=False)

    ReportingPeriod = relationship(u'ReportingPeriod')


class ReportingPeriod(Base):
    __tablename__ = 'ReportingPeriod'

    Id = Column(Integer, primary_key=True)
    Year = Column(Unicode(4), nullable=False)
    Description = Column(Unicode(250), nullable=False)
