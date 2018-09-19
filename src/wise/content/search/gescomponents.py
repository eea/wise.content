# -*- coding: utf-8 -*-

# GES criterias have been used in 2010/2012 reports and then revamped for 2018
# reports. As such, some exist in 2010 that didn't exist in 2018, some exist
# for 2018 that didn't exist for 2010 and they have changed their ids between
# the two reporting exercises.
_GES_TERMS = """
D2C2	D2C2 Established NIS	2	2.1 Abundance and state characterisation of non-indigenous species, in particular invasive species
D2C2	D2C2 Established NIS	2	2.1.1 Trends in abundance of NIS
D2C3	D2C3 Adverse effects of NIS	3	2.2 Environmental impact of invasive non-indigenous species
D2C3	D2C3 Adverse effects of NIS	3	2.2.1 Ratio invasive to native species
D2C3	D2C3 Adverse effects of NIS on species and habitats	3	2.2.2 Impacts of NIS
D3C1	D3C1 Fishing mortality rate (F)	4	3.1 Level of pressure of the fishing activity
D3C1	D3C1 Fishing mortality rate (F)	4	3.1.1 Fishing mortality
D3C1	D3C1 Fishing mortality rate (F)	4	3.1.2 Fish catch/biomass ratio
D3C2	D3C2 Spawning stock biomass (SSB)	5	3.2 Reproductive capacity of the stock
D3C2	D3C2 Spawning stock biomass (SSB)	5	3.2.1 Spawning stock biomass
D3C2	D3C2 Spawning stock biomass (SSB)	5	3.2.2 Biomass indices
D3C3	D3C3 Population age/size distribution	6	3.3 Population age and size distribution
D3C3	D3C3 Population age/size distribution	6	3.3.1 Proportion of larger fish
D3C3	D3C3 Population age/size distribution	6	3.3.3 Fish length distribution
D3C3	D3C3 Population age/size distribution	6	3.3.4 Fish size at sexual maturation
D5C1	D5C1 Nutrient concentrations	7	5.1 Nutrients level
D5C1	D5C1 Nutrient concentrations	7	5.1.1 Nutrient concentration
D5C2	D5C2 Chlorophyll-a concentration	8	5.2.1 Chlorophyll concentration
D5C3	D5C3 Harmful algal blooms	9	5.2.4 Shift in floristic species composition
D5C4	D5C4 Photic limit	10	5.2.2 Water transparency
D5C5	D5C5 Dissolved oxygen concentration	11	5.3.2 Dissolved oxygen
D5C6	D5C6 Opportunistic macroalgae of benthic habitats	12	5.2.3 Abundance of macroalgae
D5C7	D5C7 Macrophyte communities of benthic habitats	13	5.3.1 Abundance of seaweeds and seagrasses
D5C8	D5C8 Macrofaunal communities of benthic habitats	14	–
D6C1	D6C1 Physical loss of the seabed	15	6.1 Physical damage, having regard to substrate characteristics
D6C2	D6C2 Physical disturbance to the seabed	16	6.1 Physical damage, having regard to substrate characteristics
D6C3	D6C3 Adverse effects from physical disturbance	17	6.1.2 Extent of seabed affected
D7C1	D7C1 Permanent alteration of hydrographical conditions	18	7.1.1 Extent of area affected
D7C1	D7C1 Permanent alteration of hydrographical conditions	18	7.1 Spatial characterisation of permanent alterations
D7C2	D7C2 Adverse effects from permanent alteration of hydrographical conditions	19	7.2.1 Extent of habitats affected
D7C2	D7C2 Adverse effects from permanent alteration of hydrographical conditions	19	7.2.2 Change in habitats
D7C2	D7C2 Adverse effects from permanent alteration of hydrographical conditions	19	7.2 Impact of permanent hydrographical changes
D8C1	D8C1 Contaminants in environment	20	8.1.1 Concentration of contaminants
D8C1	D8C1 Contaminants in environment	20	8.1 Concentration of contaminants
D8C2	D8C2 Adverse effects of contaminants	21	8.2.1 Level of pollution effects
D8C2	D8C2 Adverse effects of contaminants	21	8.2 Effects of contaminants
D8C3	D8C3 Significant acute pollution events	22	8.2.2 Occurrence and impact of acute pollution
D8C4	D8C4 Adverse effects of significant pollution events	23	8.2.2 Occurrence and impact of acute pollution
D9C1	D9C1 Contaminants in seafood	24	9.1.1 Levels of contaminants in seafood
D9C1	D9C1 Contaminants in seafood	24	9.1 Levels, number and frequency of contaminants
D10C1	D10C1 Litter (excluding micro-litter)	25	10.1.1 Trends in litter on shore
D10C1	D10C1 Litter (excluding micro-litter)	25	10.1.2 Trends in litter in water column
D10C1	D10C1 Litter (excluding micro-litter)	25	10.1 Characteristics of litter in the marine and coastal environment
D10C2	D10C2 Micro-litter	26	10.1.3 Trends in micro-plastics
D10C2	D10C2 Micro-litter	26	10.1 Characteristics of litter in the marine and coastal environment
D10C3	D10C3 Litter ingested	27	10.2.1 Trends in amount of litter ingested
D10C3	D10C3 Litter ingested	27	10.1 Characteristics of litter in the marine and coastal environment
D10C4	D10C4 Adverse effects of litter	28	10.2 Impacts of marine litter on marine life
D11C1	D11C1 Anthropogenic impulsive sound	29	11.1.1 Proportion of days with loud sound levels
D11C1	D11C1 Anthropogenic impulsive sound	29	11.1 Distribution in time and place of loud, low and mid frequency impulsive sounds
D11C2	D11C2 Anthropogenic continuous low-frequency sound	30	11.2.1 Ambient noise
D11C2	D11C2 Anthropogenic continuous low-frequency sound	30	11.2 Continuous low frequency sound
D1C1	D1C1 Mortality rate from incidental by-catch	31	–
D1C2	D1C2 Population abundance	32	1.2.1 Population abundance
D1C2	D1C2 Population abundance	32	1.2 Population size
D1C3	D1C3 Population demographic characteristics	33	1.3.1 Population demographic characteristics
D1C3	D1C3 Population demographic characteristics	33	1.3 Population condition
D1C4	D1C4 Population distributional range and pattern	34	1.1.1 Species distributional range
D1C4	D1C4 Population distributional range and pattern	34	1.1.2 Species distributional pattern
D1C4	D1C4 Population distributional range and pattern	34	1.1 Species distribution
D1C5	D1C5 Habitat for the species	35	-
D1C6	D1C6 Pelagic habitat condition	36	1.6.1 Condition typical species
D1C6	D1C6 Pelagic habitat condition	36	1.6.3 Habitat condition
D1C6	D1C6 Pelagic habitat condition	36	1.6 Habitat condition
D1C6	D1C6 Pelagic habitat condition	36	1.6.2 Relative abundance
D6C4	D6C4 Benthic habitat extent	37	1.5.1 Habitat area
D6C4	D6C4 Benthic habitat extent	37	6.1.1 Biogenic substrata
D6C4	D6C4 Benthic habitat extent	37	1.5 Habitat extent
D6C5	D6C5 Benthic habitat condition	38	6.2 Condition of benthic community
D6C5	D6C5 Benthic habitat condition	38	1.6 Habitat condition
D6C5	D6C5 Benthic habitat condition	38	1.6.1 Condition typical species
D6C5	D6C5 Benthic habitat condition	38	1.6.2 Relative abundance
D6C5	D6C5 Benthic habitat condition	38	1.6.3 Habitat condition
D6C5	D6C5 Benthic habitat condition	38	6.2.1 Presence of sensitive species
D6C5	D6C5 Benthic habitat condition	38	6.2.2 Benthic multi-metric indexes
D6C5	D6C5 Benthic habitat condition	38	6.2.3 Proportion of individuals above specified size
D6C5	D6C5 Benthic habitat condition	38	6.2.4 Size spectrum of benthic community
D4C1	D4C1 Trophic guild species diversity	39	1.7 Ecosystem structure
D4C1	D4C1 Trophic guild species diversity	39	1.7.1 Composition ecosystem
D4C2	D4C2 Abundance across trophic guilds	40	1.7 Ecosystem structure
D4C2	D4C2 Abundance across trophic guilds	40	1.7.1 Composition ecosystem
D4C2	D4C2 Abundance across trophic guilds	40	4.3.1 Abundance trends of selected groups/species
D4C2	D4C2 Abundance across trophic guilds	40	4.3 Abundance/distribution of key trophic groups/species
D4C3	D4C3 Trophic guild size distribution	41	4.2.1 Large fish by weight
D4C3	D4C3 Trophic guild size distribution	41	4.2 Proportion of selected species at the top of food webs
D4C4	D4C4 Trophic guild productivity	42	4.1.1 Productivity of key predators
D4C4	D4C4 Trophic guild productivity	42	4.1 Productivity (production per unit biomass) of key species or trophic groups
1.1.3	1.1.3 Area covered by species	43	Y
1.3.2	1.3.2 Population genetic structure	44	Y
1.4	1.4 Habitat distribution	45	Y
1.4.1	1.4.1 Distributional range	46	Y
1.4.2	1.4.2 Distributional pattern	47	Y
1.5.2	1.5.2 Habitat volume	48	Y
3.3.2	3.3.2 Mean maximum length across all fish species found in research vessel	49	Y
5.1.2	5.1.2 Nutrient ratios (silica, nitrogen and phosphorus)	50	Y
5.2	5.2 Direct effects of nutrient enrichment	51	Y
5.3	5.3 Indirect effects of nutrient enrichment	52	Y
9.1.2	9.1.2 Frequency of regulatory levels being exceeded	53	Y
"""


class Criterion(object):
    """ A container for a GES criterion information
    """

    _id = None      # id for the 2018 version
    _title = None   # title for the 2018 version
    _alternatives = None

    def __init__(self, id, title, alternatives=None):
        self._id = id
        self._title = title
        self.alternatives = alternatives or []        # tuples of (id, title)

    def __str__(self):
        return "<Criterion {}>".format(self.title)

    def is_2018_exclusive(self):
        return not self.alternatives

    def is_2012_exclusive(self):
        return not self._id

    @property
    def id(self):
        return self._id or self.alternatives[0][0]

    @property
    def title(self):
        alter = self.alternatives

        if not alter:
            return "{} {}".format(self._id, self._title)

        if not self._id:
            id, title = alter[0]

            return "{} {}".format(id, title)

        alter_ids = len(alter) == 0 and alter[0][0] \
            or ', '.join([a[0] for a in alter])

        return "{} ({}) {}".format(
            self._id,
            alter_ids,
            self._title,
        )

    @property
    def descriptor(self):
        """ Returns the descriptor as a D<n> id
        """

        if self._id:        # 2018 version
            return self._id.split('C')[0]

        id = self.alternatives[0][0]    # 2012 version

        return 'D' + id.split('.')[0]


def parse_ges_terms(terms):
    res = []
    lines = terms.split('\n')

    for line in lines:
        line = line.strip()

        if not line:
            continue
        bits = line.split('\t')
        bits = [b.strip() for b in bits]

        b1, b2, b3, b4 = bits

        id_2012 = None
        title_2012 = None
        id_2018 = None
        title_2018 = None

        if b1.startswith('D'):
            # new style criterions. Ex:
            # D6C5	D6C5 Benthic habitat condition	38	6.2.3 Proportion of ...
            id_2018 = b1
            title_2018 = b2.split(' ', 1)[1]

            if b4[0].isdigit():
                # we also have the old criterion
                id_2012 = b4.split(' ', 1)[0]
                title_2012 = b4.split(' ', 1)[1]

            # if the criterion has already been defined, annotate that one

            seen = False

            for crit in res:
                if id_2018 and (crit.id == id_2018):
                    # already seen this criterion, let's append the title
                    seen = True
                    crit.alternatives.append((id_2012, title_2012))

            if not seen:
                crit = Criterion(id_2018, title_2018)

                if id_2012:
                    crit.alternatives.append((id_2012, title_2012))

                res.append(crit)

            continue

        if b1[0].isdigit():
            # old style criterions. Ex:
            # 5.3	5.3 Indirect effects of nutrient enrichment	52	Y
            id_2012 = b1
            title_2012 = b2.split(' ', 1)[1]

            crit = Criterion(None, None)
            crit.alternatives.append((id_2012, title_2012))
            res.append(crit)

    return res


GES_CRITERIONS = parse_ges_terms(_GES_TERMS)


def get_ges_criterions(descriptor=None):
    """ Returns a list of Criterion objects
    """

    if not descriptor:
        return GES_CRITERIONS

    return [c for c in GES_CRITERIONS if c.descriptor == descriptor]
