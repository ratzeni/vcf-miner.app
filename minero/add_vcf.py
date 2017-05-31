import sys
from minero.utils import get_conf, get_vcfminer_client, path_exists


class AddVCFWorkflow(object):
    def __init__(self, args=None, logger=None):
        self.logger = logger

        self.conf = get_conf(logger, args.config_file)
        self.vcfiminer_conf = self.conf.get_vcfminer_section()

        self.user = args.user if args.user else None
        self.group = args.group if args.group else None
        self.vcf_file = args.vcf_file

        if not self.user and not self.group:
            self.logge.error('Please define user ot group to whom VCF will be assigned')
            sys.exit()

        self.vcfminer_client = get_vcfminer_client(conf=self.vcfiminer_conf, logger=logger)

    def run(self):
        path_exists(path=self.vcf_file, logger=self.logger)

        if not self.vcfminer_client.is_connected():
            self.logger.error('Access denied')
            sys.exit()

        result = self.vcfminer_client.upload_vcf(vcfpath=self.vcf_file,
                                                 vcfname=None,
                                                 user_id=self.user,
                                                 group_id=self.group,
                                                 force_group=True)

help_doc = """
Handle the VCF upload
"""


def make_parser(parser):
    parser.add_argument('--user', metavar="STRING",
                        help="User to whom VCF will be assigned")
    parser.add_argument('--group', metavar="STRING",
                        help="Group to whom VCF will be assigned")
    parser.add_argument('--vcf_file', metavar="PATH", required=True,
                        help="VCF File to upload")


def implementation(logger, args):
    workflow = AddVCFWorkflow(args=args, logger=logger)
    workflow.run()


def do_register(registration_list):
    registration_list.append(('add_vcf', help_doc, make_parser,
                              implementation))