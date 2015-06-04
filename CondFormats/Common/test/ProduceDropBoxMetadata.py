import FWCore.ParameterSet.Config as cms

process = cms.Process("myprocess")
process.load("CondCore.CondDB.CondDB_cfi")

process.CondDBCommon.connect = 'sqlite_file:DropBoxMetadata.db'


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(1)
)
process.source = cms.Source("EmptySource",
                            firstRun = cms.untracked.uint32(300000)
                            )

# process.PoolDBOutputService.DBParameters.messageLevel = 3
import json

def encodeJsonInString(filename):
    """This function open the json file and encodes it in a string replacing probelamtic characters"""
    thefile = open(filename)
    thejson = json.load(thefile)
    thefile.close()
    return json.JSONEncoder().encode(thejson).replace('"',"&quot;")



# beamspot by run
BeamSpotObjectsRcdByRun_prod_str = encodeJsonInString("BeamSpotObjectsRcdByRun_prod.json")
BeamSpotObjectsRcdByRun_prep_str = encodeJsonInString("BeamSpotObjectsRcdByRun_prep.json")

# beamspot by lumi
BeamSpotObjectsRcdByLumi_prod_str = encodeJsonInString("BeamSpotObjectsRcdByLumi_prod.json")
BeamSpotObjectsRcdByLumi_prep_str = encodeJsonInString("BeamSpotObjectsRcdByLumi_prep.json")

#SiStripBadStripRcd
SiStripBadStripRcd_prod_str = encodeJsonInString("SiStripBadStripRcd_prod.json")
SiStripBadStripRcd_prep_str = encodeJsonInString("SiStripBadStripRcd_prep.json")

#SiStripApvGainRcd
SiStripApvGainRcd_prod_str = encodeJsonInString("SiStripApvGainRcd_prod.json")
SiStripApvGainRcd_prep_str = encodeJsonInString("SiStripApvGainRcd_prep.json")

#SiPixelAli
SiPixelAliRcd_prod_str = encodeJsonInString("SiPixelAliRcd_prod.json")
SiPixelAliRcd_prep_str = encodeJsonInString("SiPixelAliRcd_prep.json")


process.mywriter = cms.EDAnalyzer("ProduceDropBoxMetadata",
                                  write = cms.untracked.bool(False),
                                  toWrite = cms.VPSet(cms.PSet(record              = cms.untracked.string("BeamSpotObjectsRcdByRun"), 
                                                               Source              = cms.untracked.string("AlcaHarvesting"),
                                                               FileClass           = cms.untracked.string("ALCA"),
                                                               prodMetaData        = cms.untracked.string(BeamSpotObjectsRcdByRun_prod_str),
                                                               prepMetaData        = cms.untracked.string(BeamSpotObjectsRcdByRun_prep_str),
                                                               ),
                                                      cms.PSet(record              = cms.untracked.string('BeamSpotObjectsRcdByLumi'),
                                                               Source              = cms.untracked.string("AlcaHarvesting"),
                                                               FileClass           = cms.untracked.string("ALCA"),
                                                               prodMetaData        = cms.untracked.string(BeamSpotObjectsRcdByLumi_prod_str),
                                                               prepMetaData        = cms.untracked.string(BeamSpotObjectsRcdByLumi_prep_str),
                                                               ),
                                                      cms.PSet(record              = cms.untracked.string('SiStripBadStripRcd'),
                                                               Source              = cms.untracked.string("AlcaHarvesting"),
                                                               FileClass           = cms.untracked.string("ALCA"),
                                                               prodMetaData        = cms.untracked.string(SiStripBadStripRcd_prod_str),
                                                               prepMetaData        = cms.untracked.string(SiStripBadStripRcd_prep_str),
                                                               ),
                                                      cms.PSet(record              = cms.untracked.string('SiStripApvGainRcd'),
                                                               Source              = cms.untracked.string("AlcaHarvesting"),
                                                               FileClass           = cms.untracked.string("ALCA"),
                                                               prodMetaData        = cms.untracked.string(SiStripApvGainRcd_prod_str),
                                                               prepMetaData        = cms.untracked.string(SiStripApvGainRcd_prep_str),
                                                               ),
                                                      cms.PSet(record              = cms.untracked.string('SiPixelAliRcd'),
                                                               Source              = cms.untracked.string("AlcaHarvesting"),
                                                               FileClass           = cms.untracked.string("ALCA"),
                                                               prodMetaData        = cms.untracked.string(SiPixelAliRcd_prod_str),
                                                               prepMetaData        = cms.untracked.string(SiPixelAliRcd_prep_str),
                                                               )

                                                      ),
                                  read = cms.untracked.bool(True),
                                  toRead = cms.untracked.vstring("BeamSpotObjectsRcdByRun",'BeamSpotObjectsRcdByLumi','SiStripBadStripRcd','SiStripApvGainRcd','SiPixelAliRcd') # same strings as fType
                                  )


process.p = cms.Path(process.mywriter)

if process.mywriter.write:

    from CondCore.DBCommon.CondDBCommon_cfi import CondDBCommon
    CondDBCommon.connect = "sqlite_file:DropBoxMetadata.db"

    process.PoolDBOutputService = cms.Service("PoolDBOutputService",
                                      CondDBCommon,
                                      toPut = cms.VPSet(cms.PSet(record = cms.string('DropBoxMetadataRcd'),
                                                                 tag = cms.string('DropBoxMetadata'),
                                                                 timetype   = cms.untracked.string('runnumber')
                                                                 )
                                                                 ),
                                      loadBlobStreamer = cms.untracked.bool(False),
                                      #    timetype   = cms.untracked.string('lumiid')
                                      #    timetype   = cms.untracked.string('runnumber')
                                      )

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.GlobalTag.globaltag = 'GR_E_V48'
process.GlobalTag.connect   = 'frontier://PromptProd/CMS_CONDITIONS'
#process.GlobalTag.connect   = 'sqlite_file:/afs/cern.ch/user/c/cerminar/public/Alca/GlobalTag/GR_R_311_V2.db'


readsqlite = True
if readsqlite:
    process.GlobalTag.toGet = cms.VPSet(
        cms.PSet(record = cms.string("DropBoxMetadataRcd"),
                 tag = cms.string("DropBoxMetadata"),
                 connect = cms.untracked.string("sqlite_file:DropBoxMetadata.db")
                )
        )
