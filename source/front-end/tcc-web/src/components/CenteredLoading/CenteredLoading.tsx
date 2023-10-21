import { CenterDiv } from './styles';
import { CircularProgress } from '@mui/material';

type Props = {
  show: boolean;
}

const CenteredLoading = ({ show }: Props) => {
  return (
    <>
      {show && <CenterDiv>
        <CircularProgress />
      </CenterDiv>}
    </>
  )
}

export default CenteredLoading