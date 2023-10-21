import styled from 'styled-components';

export const JobOverviewCard = styled.div`
  width: 95%;
  height: 11%;
  padding: 3% 4%;
  box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);

  &:hover {
    transition-duration: 0.5s;
    background-color: #E1E1E1;
    cursor: pointer;
  }
`

export const JobOverviewCardHeader = styled.div`
  display: flex;
  justify-content: space-between;
`
